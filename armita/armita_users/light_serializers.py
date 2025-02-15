from rest_framework import serializers
from .models import User, JobListing

class UserLightSerializer(serializers.ModelSerializer):
    """Returns only essential user details to reduce response size."""
    class Meta:
        model = User
        fields = ['id', 'username', 'user_type', 'location']

class JobListingLightSerializer(serializers.ModelSerializer):
    """Returns essential job details without full descriptions."""
    client = UserLightSerializer(read_only=True)

    class Meta:
        model = JobListing
        fields = ['id', 'title', 'category', 'budget', 'location', 'client']
