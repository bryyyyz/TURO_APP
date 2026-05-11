import mimetypes
import os
import posixpath
import secrets
from urllib.parse import quote

import requests
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


def _clean_base(url: str) -> str:
    return str(url or "").rstrip("/")


@deconstructible
class SupabaseStorage(Storage):
    """
    Minimal Django Storage backend for Supabase Storage.

    This is intentionally small: we only need save(), delete(), exists(), and url()
    for FileField/ImageField usage in this project.
    """

    def __init__(self, supabase_url=None, service_role_key=None, bucket=None, public=True):
        self.supabase_url = _clean_base(supabase_url or os.environ.get("SUPABASE_URL"))
        self.service_role_key = service_role_key or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        self.bucket = bucket or os.environ.get("SUPABASE_STORAGE_BUCKET", "turo-media")
        self.public = str(os.environ.get("SUPABASE_STORAGE_PUBLIC", str(public))).lower() in {"1", "true", "yes"}

        if not self.supabase_url or not self.service_role_key or not self.bucket:
            raise ValueError("SupabaseStorage requires SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_STORAGE_BUCKET")

    def _headers(self, content_type=None):
        h = {
            "Authorization": f"Bearer {self.service_role_key}",
            "apikey": self.service_role_key,
        }
        if content_type:
            h["Content-Type"] = content_type
        return h

    def _object_path(self, name: str) -> str:
        # Normalize to posix paths for object keys
        name = str(name).lstrip("/").replace("\\", "/")
        return name

    def _upload_url(self, key: str) -> str:
        # POST will fail if object exists; we use PUT to upsert/overwrite
        return f"{self.supabase_url}/storage/v1/object/{self.bucket}/{quote(key)}"

    def _public_url(self, key: str) -> str:
        # This assumes the bucket is public.
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket}/{quote(key)}"

    def _signed_url(self, key: str, expires_in: int = 60 * 60 * 24 * 7) -> str:
        """
        Generate a signed URL for private buckets.
        """
        url = f"{self.supabase_url}/storage/v1/object/sign/{self.bucket}/{quote(key)}"
        r = requests.post(url, headers=self._headers("application/json"), json={"expiresIn": int(expires_in)}, timeout=15)
        if r.status_code >= 400:
            raise IOError(f"Supabase signed URL failed ({r.status_code}): {r.text[:300]}")
        data = r.json() if r.content else {}
        signed_path = data.get("signedURL") or data.get("signedUrl")
        if not signed_path:
            raise IOError("Supabase signed URL response missing signedURL")
        # signedURL is usually a path starting with /storage/v1/...
        if str(signed_path).startswith("http"):
            return signed_path
        signed_path = str(signed_path)
        # Some Supabase responses return "/object/sign/..." (without /storage/v1).
        if signed_path.startswith("/object/"):
            signed_path = f"/storage/v1{signed_path}"
        return f"{self.supabase_url}{signed_path}"

    def _save(self, name, content):
        key = self._object_path(name)

        # Ensure unique name if collision
        if self.exists(key):
            root, ext = os.path.splitext(key)
            key = f"{root}-{secrets.token_hex(4)}{ext}"

        content.open("rb")
        data = content.read()
        content_type = getattr(content, "content_type", None) or mimetypes.guess_type(key)[0] or "application/octet-stream"

        r = requests.put(self._upload_url(key), headers=self._headers(content_type), data=data, timeout=30)
        if r.status_code >= 400:
            raise IOError(f"Supabase upload failed ({r.status_code}): {r.text[:300]}")
        return key

    def delete(self, name):
        key = self._object_path(name)
        url = f"{self.supabase_url}/storage/v1/object/{self.bucket}/{quote(key)}"
        r = requests.delete(url, headers=self._headers(), timeout=30)
        # Supabase returns 200/204 when deleted; ignore missing
        if r.status_code not in {200, 204, 404}:
            raise IOError(f"Supabase delete failed ({r.status_code}): {r.text[:300]}")

    def exists(self, name):
        key = self._object_path(name)
        url = f"{self.supabase_url}/storage/v1/object/info/{self.bucket}/{quote(key)}"
        r = requests.get(url, headers=self._headers(), timeout=15)
        if r.status_code == 200:
            return True
        if r.status_code == 404:
            return False
        # For any other error, assume it doesn't exist to avoid blocking uploads
        return False

    def url(self, name):
        key = self._object_path(name)
        # If the object is missing in Supabase (common right after switching from local MEDIA_ROOT),
        # fall back to local /media/ URL so existing deployments can still serve old files.
        if not self.exists(key):
            return f"/media/{quote(key)}"

        if self.public:
            return self._public_url(key)
        return self._signed_url(key)

    def get_available_name(self, name, max_length=None):
        # We'll handle collisions in _save
        name = self._object_path(name)
        if max_length and len(name) > max_length:
            dirn, fn = posixpath.split(name)
            root, ext = os.path.splitext(fn)
            keep = max(1, max_length - len(dirn) - len(ext) - 2)
            name = posixpath.join(dirn, f"{root[:keep]}{ext}")
        return name

