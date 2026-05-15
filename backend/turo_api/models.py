from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('tutor', 'Tutor'),
    )
    TUTOR_TIER_CHOICES = (
        ('basic', 'Tier 1 - Basic Tutor'),
        ('plus', 'Tier 2 - Plus Tutor'),
        ('pro', 'Tier 3 - Pro Tutor'),
    )
    TIER_REVIEW_STATUS_CHOICES = (
        ('not_submitted', 'Not Submitted'),
        ('pending', 'Pending Admin Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    tutor_tier = models.CharField(max_length=20, choices=TUTOR_TIER_CHOICES, default='basic')
    tier_review_status = models.CharField(max_length=20, choices=TIER_REVIEW_STATUS_CHOICES, default='not_submitted')
    tier_review_submitted_at = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    name_extension = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    bio = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    credentials_document = models.FileField(upload_to='tutor_credentials/', blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    barangay = models.CharField(max_length=200, blank=True)
    municipality = models.CharField(max_length=200, blank=True)
    province = models.CharField(max_length=200, blank=True)
    id_photo = models.ImageField(upload_to='id_photos/', blank=True, null=True)
    requires_id_verification = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class ProfileCredentialDocument(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='credential_documents')
    file = models.FileField(upload_to='tutor_credentials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at', '-id']

    def __str__(self):
        return f"Credential file for profile #{self.profile_id}"

class ExpertisePost(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, default='Untitled')
    subject = models.CharField(max_length=100)
    description = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    level = models.CharField(max_length=50, default='All Levels')
    total_sessions = models.PositiveIntegerField(default=1)
    photo = models.ImageField(upload_to='post_photos/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.tutor.username}"

class SessionSlot(models.Model):
    """Specific date+time options a tutor offers for each session number in a listing."""
    post = models.ForeignKey(ExpertisePost, on_delete=models.CASCADE, related_name='session_slots')
    session_number = models.PositiveIntegerField(default=1)  # Which session in the sequence
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ['session_number', 'date', 'start_time']
        unique_together = ('post', 'session_number', 'date', 'start_time')

    def __str__(self):
        return f"{self.post.title} — Session {self.session_number} · {self.date} {self.start_time}"

class TutorAvailability(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name_plural = "Tutor Availabilities"
        unique_together = ('tutor', 'day_of_week', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.tutor.username} - {self.get_day_of_week_display()} ({self.start_time}-{self.end_time})"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_bookings')
    expertise_post = models.ForeignKey(ExpertisePost, on_delete=models.CASCADE, null=True, blank=True)
    session_slot = models.ForeignKey(SessionSlot, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    session_number = models.PositiveIntegerField(default=1)
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} with {self.tutor.username} — {self.date}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp}"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('gcash', 'GCash'),
        ('visa', 'Visa/Credit Card'),
        ('cash', 'Cash'),
    )
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='completed')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='gcash')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Payment for {self.booking}"
