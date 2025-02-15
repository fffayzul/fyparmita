from rest_framework import serializers
from .models import User, ArtisanProfile, JobListing, JobApplication, Transaction, Review, Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ArtisanProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ArtisanProfile
        fields = '__all__'

class JobListingSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)

    class Meta:
        model = JobListing
        fields = '__all__'

class JobApplicationSerializer(serializers.ModelSerializer):
    artisan = UserSerializer(read_only=True)
    job = JobListingSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
