from django.db.models import Q
from rest_framework import viewsets, permissions, response, status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Profile, ProfileCredentialDocument, ExpertisePost, SessionSlot, TutorAvailability, Booking, Message, Payment
from .serializers import (ProfileSerializer, ExpertisePostSerializer, SessionSlotSerializer,
                          TutorAvailabilitySerializer, BookingSerializer,
                          MessageSerializer, PaymentSerializer)

ADMIN_PANEL_USERNAME = 'admin'
ADMIN_PANEL_PASSWORD = 'admin123'


def _is_admin_panel_authenticated(request):
    header_username = request.headers.get('X-Admin-Username')
    header_password = request.headers.get('X-Admin-Password')
    body_username = request.data.get('username') if hasattr(request, 'data') else None
    body_password = request.data.get('password') if hasattr(request, 'data') else None

    username = header_username or body_username
    password = header_password or body_password
    return username == ADMIN_PANEL_USERNAME and password == ADMIN_PANEL_PASSWORD

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        qs = self.queryset
        email = self.request.query_params.get('email')
        role  = self.request.query_params.get('role')
        
        if email:
            # Try to find the user
            user = User.objects.filter(email=email).first()
            if not user:
                # If user doesn't exist in Django, create them using email as username
                username = email.split('@')[0]
                # Ensure username is unique
                if User.objects.filter(username=username).exists():
                    import uuid
                    username = f"{username}_{uuid.uuid4().hex[:4]}"
                user = User.objects.create(username=username, email=email)
            
            # Ensure profile exists; sync role when client passes role (tutor vs student dashboard)
            user_profile, _created = Profile.objects.get_or_create(
                user=user, defaults={'role': role or 'student'}
            )
            if role and user_profile.role != role:
                user_profile.role = role
                user_profile.save(update_fields=['role'])

            qs = qs.filter(user__email=email)

        if role:
            qs = qs.filter(role=role)
            
        return qs

    def partial_update(self, request, *args, **kwargs):
        profile = self.get_object()
        files = request.FILES.getlist('credentials_documents')
        response_obj = super().partial_update(request, *args, **kwargs)

        if files:
            profile.credential_documents.all().delete()
            created = []
            for f in files:
                created.append(ProfileCredentialDocument.objects.create(profile=profile, file=f))

            first_file = created[0].file if created else None
            if first_file:
                profile.credentials_document = first_file
                profile.save(update_fields=['credentials_document'])

            serializer = self.get_serializer(profile)
            return response.Response(serializer.data, status=response_obj.status_code)

        return response_obj

class ExpertisePostViewSet(viewsets.ModelViewSet):
    queryset = ExpertisePost.objects.select_related('tutor', 'tutor__profile').prefetch_related('session_slots')
    serializer_class = ExpertisePostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = self.queryset
        municipality = self.request.query_params.get('municipality')
        province = self.request.query_params.get('province')
        tutor_id = self.request.query_params.get('tutor_id')
        email = self.request.query_params.get('email')
        region_match = (self.request.query_params.get('region_match') or '').strip()

        if municipality:
            qs = qs.filter(tutor__profile__municipality__icontains=municipality)
        if province:
            qs = qs.filter(tutor__profile__province__icontains=province)
        if tutor_id:
            qs = qs.filter(tutor_id=tutor_id)
        if email:
            qs = qs.filter(tutor__email=email)

        # Discover: student province vs tutor province OR municipality (tokens for "Cebu" vs "Cebu Province")
        if region_match:
            _stop = {'city', 'province', 'the', 'of', 'and'}
            loc_q = (
                Q(tutor__profile__province__icontains=region_match)
                | Q(tutor__profile__municipality__icontains=region_match)
            )
            for part in region_match.replace(',', ' ').replace('-', ' ').split():
                token = part.strip()
                if len(token) >= 3 and token.lower() not in _stop:
                    loc_q |= (
                        Q(tutor__profile__province__icontains=token)
                        | Q(tutor__profile__municipality__icontains=token)
                    )
            qs = qs.filter(loc_q)

        return qs.order_by('-created_at')

class SessionSlotViewSet(viewsets.ModelViewSet):
    queryset = SessionSlot.objects.all()
    serializer_class = SessionSlotSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        post_id  = self.request.query_params.get('post_id')
        tutor_id = self.request.query_params.get('tutor_id')
        if post_id:
            return self.queryset.filter(post_id=post_id)
        if tutor_id:
            return self.queryset.filter(post__tutor_id=tutor_id)
        return self.queryset

class TutorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = TutorAvailability.objects.all()
    serializer_class = TutorAvailabilitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tutor_id = self.request.query_params.get('tutor_id')
        if tutor_id:
            return self.queryset.filter(tutor_id=tutor_id)
        return self.queryset

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related(
        'student', 'student__profile', 'tutor', 'expertise_post', 'session_slot'
    ).all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        student_id = self.request.query_params.get('student_id')
        tutor_id   = self.request.query_params.get('tutor_id')
        if student_id:
            return self.queryset.filter(student_id=student_id)
        if tutor_id:
            return self.queryset.filter(tutor_id=tutor_id)
        return self.queryset

    def perform_create(self, serializer):
        booking = serializer.save()
        # Mark the linked session slot as booked
        if booking.session_slot:
            booking.session_slot.is_booked = True
            booking.session_slot.save()

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('booking__student', 'booking__tutor', 'booking__expertise_post').all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = self.queryset
        tutor_id   = self.request.query_params.get('tutor_id')
        student_id = self.request.query_params.get('student_id')
        if tutor_id:
            qs = qs.filter(booking__tutor_id=tutor_id)
        if student_id:
            qs = qs.filter(booking__student_id=student_id)
        return qs.order_by('-paid_at')


class AdminTierRequestsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if not _is_admin_panel_authenticated(request):
            return response.Response(
                {'detail': 'Unauthorized admin access.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        pending = (
            Profile.objects.select_related('user').prefetch_related('credential_documents')
            .filter(role='tutor', tier_review_status='pending')
            .order_by('-tier_review_submitted_at', '-id')
        )
        items = []
        for p in pending:
            credentials_document_url = None
            if p.credentials_document:
                credentials_document_url = request.build_absolute_uri(p.credentials_document.url)
            credentials_documents = [
                {
                    'id': d.id,
                    'name': d.file.name.split('/')[-1],
                    'url': request.build_absolute_uri(d.file.url),
                }
                for d in p.credential_documents.all()
            ]
            avatar_url = None
            if p.avatar:
                avatar_url = request.build_absolute_uri(p.avatar.url)

            items.append({
                'id': p.id,
                'user_id': p.user_id,
                'email': p.user.email,
                'first_name': p.first_name,
                'last_name': p.last_name,
                'bio': p.bio or '',
                'achievements': p.achievements or '',
                'current_tier': p.tutor_tier,
                'tier_review_status': p.tier_review_status,
                'tier_review_submitted_at': p.tier_review_submitted_at,
                'credentials_document_url': credentials_document_url,
                'credentials_documents': credentials_documents,
                'avatar_url': avatar_url,
            })

        return response.Response(items, status=status.HTTP_200_OK)


class AdminTierDecisionView(APIView):
    permission_classes = [permissions.AllowAny]

    def patch(self, request, profile_id):
        if not _is_admin_panel_authenticated(request):
            return response.Response(
                {'detail': 'Unauthorized admin access.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        profile = Profile.objects.filter(id=profile_id, role='tutor').first()
        if not profile:
            return response.Response(
                {'detail': 'Tutor profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        action = (request.data.get('action') or '').strip().lower()

        if action not in {'approve', 'reject'}:
            return response.Response(
                {'detail': 'Action must be approve or reject.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if action == 'approve':
            if profile.tutor_tier != 'basic':
                return response.Response(
                    {'detail': 'This tutor already used the one-time tier upgrade.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            profile.tier_review_status = 'approved'
        else:
            profile.tier_review_status = 'rejected'

        profile.save(update_fields=['tier_review_status'])
        return response.Response(
            {
                'id': profile.id,
                'tutor_tier': profile.tutor_tier,
                'tier_review_status': profile.tier_review_status,
            },
            status=status.HTTP_200_OK
        )
