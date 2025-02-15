from django.contrib import admin
from .models import User, ArtisanProfile, JobListing, JobApplication, Transaction, Review, Notification

# Register your models here.

admin.site.register(User)
admin.site.register(ArtisanProfile)
admin.site.register(JobListing)
admin.site.register(JobApplication)
admin.site.register(Transaction)
admin.site.register(Review)
admin.site.register(Notification)