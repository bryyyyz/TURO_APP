import os

from django.core.management.base import BaseCommand
from django.db import transaction

from turo_api.models import ExpertisePost, Profile, ProfileCredentialDocument


class Command(BaseCommand):
    help = "Upload existing local MEDIA_ROOT files into the currently configured default storage (e.g. Supabase)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print what would be uploaded without modifying anything.",
        )

    def _backfill_field(self, instance, field_name: str, dry_run: bool) -> int:
        f = getattr(instance, field_name, None)
        if not f or not getattr(f, "name", None):
            return 0

        name = f.name
        storage = f.storage

        # If it already exists in the target storage, nothing to do
        try:
            if storage.exists(name):
                return 0
        except Exception:
            # If exists check fails, try to save anyway.
            pass

        # Only works if the file is present locally (MEDIA_ROOT)
        try:
            local_path = f.path
        except Exception:
            local_path = None

        if not local_path or not os.path.exists(local_path):
            self.stdout.write(self.style.WARNING(f"Missing local file for {instance.__class__.__name__}#{instance.pk} {field_name}: {name}"))
            return 0

        self.stdout.write(f"Uploading {instance.__class__.__name__}#{instance.pk} {field_name}: {name}")
        if dry_run:
            return 1

        # Re-save the same file content to the configured storage
        with open(local_path, "rb") as fp:
            f.save(name, fp, save=True)
        return 1

    def handle(self, *args, **options):
        dry_run = bool(options["dry_run"])
        total = 0

        with transaction.atomic():
            for p in Profile.objects.all():
                total += self._backfill_field(p, "avatar", dry_run)
                total += self._backfill_field(p, "credentials_document", dry_run)

            for d in ProfileCredentialDocument.objects.all():
                total += self._backfill_field(d, "file", dry_run)

            for post in ExpertisePost.objects.all():
                total += self._backfill_field(post, "photo", dry_run)

            if dry_run:
                transaction.set_rollback(True)

        self.stdout.write(self.style.SUCCESS(f"Backfill complete. Uploaded: {total} file(s)."))

