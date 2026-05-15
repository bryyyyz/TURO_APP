from datetime import datetime

from django.utils import timezone
from pathlib import Path
from django.db import DatabaseError
from django.core.files.storage.handler import InvalidStorageError
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, ProfileCredentialDocument, ExpertisePost, SessionSlot, TutorAvailability, Booking, Message, Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class ProfileSerializer(serializers.ModelSerializer):
    email      = serializers.EmailField(source='user.email', read_only=True)
    username   = serializers.CharField(source='user.username', read_only=True)
    avatar_url = serializers.SerializerMethodField(read_only=True)
    avatar     = serializers.ImageField(required=False, allow_null=True, write_only=True)
    id_photo_url = serializers.SerializerMethodField(read_only=True)
    id_photo   = serializers.ImageField(required=False, allow_null=True, write_only=True)
    credentials_document_url = serializers.SerializerMethodField(read_only=True)
    credentials_documents = serializers.SerializerMethodField(read_only=True)
    credentials_document = serializers.FileField(required=False, allow_null=True, write_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'role', 'tutor_tier', 'tier_review_status', 'tier_review_submitted_at',
                  'phone', 'bio', 'achievements',
                  'credentials_document', 'credentials_document_url', 'credentials_documents',
                  'avatar', 'avatar_url',
                  'id_photo', 'id_photo_url', 'requires_id_verification', 'id_verification_status',
                  'first_name', 'last_name', 'middle_name', 'name_extension',
                  'barangay', 'municipality', 'province',
                  'email', 'username')

    def _abs(self, request, url: str | None):
        if not url:
            return None
        if str(url).startswith(('http://', 'https://')):
            return str(url)
        return request.build_absolute_uri(str(url)) if request else str(url)

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if not obj.avatar:
            return None
        try:
            return self._abs(request, obj.avatar.url)
        except (OSError, ValueError, InvalidStorageError):
            return None

    def get_id_photo_url(self, obj):
        request = self.context.get('request')
        if not obj.id_photo:
            return None
        try:
            return self._abs(request, obj.id_photo.url)
        except (OSError, ValueError, InvalidStorageError):
            return None

    def get_credentials_document_url(self, obj):
        request = self.context.get('request')
        if not obj.credentials_document:
            return None
        try:
            return self._abs(request, obj.credentials_document.url)
        except (OSError, ValueError, InvalidStorageError):
            return None

    def get_credentials_documents(self, obj):
        request = self.context.get('request')
        docs = []
        try:
            for d in obj.credential_documents.all():
                try:
                    file_url = self._abs(request, d.file.url)
                except (OSError, ValueError, InvalidStorageError):
                    continue
                docs.append({
                    'id': d.id,
                    'name': Path(d.file.name).name,
                    'url': file_url,
                })
        except DatabaseError:
            # Backward-compatible fallback when the credential documents table
            # has not yet been migrated in the deployed environment.
            return []
        return docs

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        new_status = validated_data.get('tier_review_status')
        if new_status == 'pending' and not instance.tier_review_submitted_at:
            validated_data['tier_review_submitted_at'] = timezone.now()

        if user_data:
            user.save()

        return super().update(instance, validated_data)

class SessionSlotSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = SessionSlot
        fields = ('id', 'post', 'post_title', 'session_number', 'date', 'start_time', 'end_time', 'is_booked')

class ExpertisePostSerializer(serializers.ModelSerializer):
    tutor_profile  = UserSerializer(source='tutor', read_only=True)
    tutor_id       = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='tutor'
    )
    photo_url      = serializers.SerializerMethodField()
    session_slots  = SessionSlotSerializer(many=True, read_only=True)

    tutor_barangay     = serializers.SerializerMethodField()
    tutor_municipality = serializers.SerializerMethodField()
    tutor_province     = serializers.SerializerMethodField()
    tutor_avatar_url   = serializers.SerializerMethodField()
    tutor_bio          = serializers.SerializerMethodField()
    tutor_achievements = serializers.SerializerMethodField()
    tutor_first_name   = serializers.SerializerMethodField()
    tutor_last_name    = serializers.SerializerMethodField()
    tutor_tier         = serializers.SerializerMethodField()

    class Meta:
        model = ExpertisePost
        fields = ('id', 'tutor_profile', 'tutor_id', 'title', 'subject',
                  'description', 'hourly_rate', 'level', 'total_sessions',
                  'photo', 'photo_url', 'session_slots',
                  'tutor_barangay', 'tutor_municipality', 'tutor_province',
                  'tutor_avatar_url', 'tutor_bio', 'tutor_achievements',
                  'tutor_first_name', 'tutor_last_name', 'tutor_tier',
                  'is_published', 'created_at')
        extra_kwargs = {'photo': {'required': False}}

    def _tutor_profile_row(self, obj):
        try:
            return obj.tutor.profile
        except Profile.DoesNotExist:
            return None

    def get_tutor_barangay(self, obj):
        p = self._tutor_profile_row(obj)
        return (p.barangay or '') if p else ''

    def get_tutor_municipality(self, obj):
        p = self._tutor_profile_row(obj)
        return (p.municipality or '') if p else ''

    def get_tutor_province(self, obj):
        p = self._tutor_profile_row(obj)
        return (p.province or '') if p else ''

    def get_tutor_avatar_url(self, obj):
        request = self.context.get('request')
        p = self._tutor_profile_row(obj)
        if p and p.avatar:
            try:
                url = p.avatar.url
            except (OSError, ValueError, InvalidStorageError):
                return None
            if str(url).startswith(('http://', 'https://')):
                return str(url)
            return request.build_absolute_uri(str(url)) if request else str(url)
        return None

    def get_tutor_bio(self, obj):
        p = self._tutor_profile_row(obj)
        return (p.bio or '') if p else ''

    def get_tutor_achievements(self, obj):
        p = self._tutor_profile_row(obj)
        return (p.achievements or '') if p else ''

    def get_tutor_first_name(self, obj):
        p = self._tutor_profile_row(obj)
        return (p.first_name or '').strip() if p else ''

    def get_tutor_last_name(self, obj):
        p = self._tutor_profile_row(obj)
        return (p.last_name or '').strip() if p else ''

    def get_tutor_tier(self, obj):
        p = self._tutor_profile_row(obj)
        return (p.tutor_tier or 'basic') if p else 'basic'

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.photo:
            try:
                url = obj.photo.url
            except (OSError, ValueError, InvalidStorageError):
                return None
            if str(url).startswith(('http://', 'https://')):
                return str(url)
            return request.build_absolute_uri(str(url)) if request else str(url)
        return None

class TutorAvailabilitySerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = TutorAvailability
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    tutor_name   = serializers.SerializerMethodField()
    student_avatar_url = serializers.SerializerMethodField()
    post_title   = serializers.CharField(source='expertise_post.title', read_only=True, default='')
    post_subject = serializers.CharField(source='expertise_post.subject', read_only=True, default='')
    student_barangay     = serializers.SerializerMethodField()
    student_municipality = serializers.SerializerMethodField()
    student_province     = serializers.SerializerMethodField()
    tutor_avatar_url     = serializers.SerializerMethodField()
    tutor_tier           = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ('id', 'student', 'tutor', 'expertise_post', 'session_slot',
                  'session_number', 'date', 'start_time', 'end_time', 'status',
                  'student_name', 'tutor_name', 'post_title', 'post_subject', 'created_at',
                  'student_barangay', 'student_municipality', 'student_province',
                  'student_avatar_url', 'tutor_avatar_url', 'tutor_tier')

    def _student_profile(self, obj):
        try:
            return obj.student.profile
        except Profile.DoesNotExist:
            return None

    def get_student_barangay(self, obj):
        p = self._student_profile(obj)
        return (p.barangay or '') if p else ''

    def get_student_municipality(self, obj):
        p = self._student_profile(obj)
        return (p.municipality or '') if p else ''

    def get_student_province(self, obj):
        p = self._student_profile(obj)
        return (p.province or '') if p else ''

    def get_student_name(self, obj):
        p = self._student_profile(obj)
        profile_name = f"{(p.first_name or '').strip()} {(p.last_name or '').strip()}".strip() if p else ''
        return profile_name or obj.student.get_full_name() or obj.student.username

    def get_tutor_name(self, obj):
        try:
            p = obj.tutor.profile
        except Profile.DoesNotExist:
            p = None
        profile_name = f"{(p.first_name or '').strip()} {(p.last_name or '').strip()}".strip() if p else ''
        return profile_name or obj.tutor.get_full_name() or obj.tutor.username

    def get_student_avatar_url(self, obj):
        request = self.context.get('request')
        p = self._student_profile(obj)
        if p and p.avatar and request:
            return request.build_absolute_uri(p.avatar.url)
        return None

    def get_tutor_avatar_url(self, obj):
        request = self.context.get('request')
        try:
            p = obj.tutor.profile
        except Profile.DoesNotExist:
            return None
        if p and p.avatar and request:
            try:
                return request.build_absolute_uri(p.avatar.url)
            except (OSError, ValueError):
                return None
        return None

    def get_tutor_tier(self, obj):
        try:
            p = obj.tutor.profile
            return p.tutor_tier or 'basic'
        except Profile.DoesNotExist:
            return 'basic'

    def validate(self, attrs):
        inst = self.instance
        if not inst:
            return attrs
        new_status = attrs.get('status', inst.status)
        if new_status != 'completed' or inst.status == 'completed':
            return attrs

        tutor_id = self.initial_data.get('tutor_id')
        try:
            tutor_id = int(tutor_id)
        except (TypeError, ValueError):
            tutor_id = None
        if tutor_id != inst.tutor_id:
            raise serializers.ValidationError(
                {'tutor_id': 'Tutor must match this booking to mark it completed.'}
            )
        if inst.status != 'confirmed':
            raise serializers.ValidationError(
                {'status': 'Only confirmed bookings can be marked completed.'}
            )
        if not inst.date or not inst.end_time:
            raise serializers.ValidationError(
                {'status': 'Booking is missing date or end time.'}
            )
        end_dt = datetime.combine(inst.date, inst.end_time)
        tz = timezone.get_current_timezone()
        if timezone.is_naive(end_dt):
            end_dt = timezone.make_aware(end_dt, tz)
        if end_dt > timezone.now():
            raise serializers.ValidationError(
                {'status': 'The session end time has not passed yet.'}
            )
        return attrs

class MessageSerializer(serializers.ModelSerializer):
    sender_name        = serializers.SerializerMethodField()
    receiver_name      = serializers.SerializerMethodField()
    sender_avatar_url  = serializers.SerializerMethodField()
    receiver_avatar_url = serializers.SerializerMethodField()
    sender_user_id     = serializers.IntegerField(source='sender_id', read_only=True)
    receiver_user_id   = serializers.IntegerField(source='receiver_id', read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'sender_user_id', 'receiver_user_id',
                  'sender_name', 'receiver_name', 'sender_avatar_url', 'receiver_avatar_url',
                  'content', 'timestamp', 'is_read')

    def validate_content(self, value):
        import re
        # Censor email addresses
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        value = re.sub(email_pattern, '[EMAIL REMOVED]', value)
        
        # Censor Philippine mobile numbers
        # Matches: 0 or 63 or +63 followed by exactly 10 digits (ignoring spaces/dashes)
        phone_pattern = r'(?:\+63|63|0)(?:[-\s]*\d){10}'
        value = re.sub(phone_pattern, '[NUMBER REMOVED]', value)
        
        return value

    def _profile_name(self, user):
        try:
            p = user.profile
            name = f"{(p.first_name or '').strip()} {(p.last_name or '').strip()}".strip()
            return name or user.get_full_name() or user.username
        except Profile.DoesNotExist:
            return user.get_full_name() or user.username

    def _profile_avatar(self, user):
        request = self.context.get('request')
        try:
            p = user.profile
            if p.avatar and request:
                try:
                    url = p.avatar.url
                    if str(url).startswith(('http://', 'https://')):
                        return str(url)
                    return request.build_absolute_uri(str(url))
                except (OSError, ValueError):
                    return None
        except Profile.DoesNotExist:
            pass
        return None

    def get_sender_name(self, obj):
        return self._profile_name(obj.sender)

    def get_receiver_name(self, obj):
        return self._profile_name(obj.receiver)

    def get_sender_avatar_url(self, obj):
        return self._profile_avatar(obj.sender)

    def get_receiver_avatar_url(self, obj):
        return self._profile_avatar(obj.receiver)

class PaymentSerializer(serializers.ModelSerializer):
    student_name  = serializers.SerializerMethodField()
    tutor_name    = serializers.SerializerMethodField()
    student_avatar_url = serializers.SerializerMethodField()
    post_subject  = serializers.CharField(source='booking.expertise_post.subject', read_only=True, default='')
    post_title    = serializers.CharField(source='booking.expertise_post.title', read_only=True, default='')
    booking_date  = serializers.DateField(source='booking.date', read_only=True)
    student_id    = serializers.IntegerField(source='booking.student_id', read_only=True)
    tutor_id      = serializers.IntegerField(source='booking.tutor_id', read_only=True)

    class Meta:
        model = Payment
        fields = ('id', 'booking', 'amount', 'paid_at', 'transaction_id',
                  'status', 'payment_method', 'notes',
                  'student_name', 'tutor_name', 'post_subject', 'post_title',
                  'booking_date', 'student_id', 'tutor_id', 'student_avatar_url')

    def get_student_name(self, obj):
        try:
            p = obj.booking.student.profile
        except Profile.DoesNotExist:
            p = None
        profile_name = f"{(p.first_name or '').strip()} {(p.last_name or '').strip()}".strip() if p else ''
        return profile_name or obj.booking.student.get_full_name() or obj.booking.student.username

    def get_tutor_name(self, obj):
        try:
            p = obj.booking.tutor.profile
        except Profile.DoesNotExist:
            p = None
        profile_name = f"{(p.first_name or '').strip()} {(p.last_name or '').strip()}".strip() if p else ''
        return profile_name or obj.booking.tutor.get_full_name() or obj.booking.tutor.username

    def get_student_avatar_url(self, obj):
        request = self.context.get('request')
        try:
            p = obj.booking.student.profile
        except Profile.DoesNotExist:
            p = None
        if p and p.avatar and request:
            return request.build_absolute_uri(p.avatar.url)
        return None
