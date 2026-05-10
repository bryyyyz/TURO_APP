from django.contrib import admin
from .models import Profile, ExpertisePost, TutorAvailability, Booking, Message, Payment

admin.site.register(Profile)
admin.site.register(ExpertisePost)
admin.site.register(TutorAvailability)
admin.site.register(Booking)
admin.site.register(Message)
admin.site.register(Payment)
