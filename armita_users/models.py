from django.db import models

# Create your models here.
class ArtisanProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artisan_profile')
    profession = models.CharField(max_length=255)  # Example: Plumber, Electrician
    bio = models.TextField(null=True, blank=True)
    skills = models.TextField(help_text="Comma-separated list of skills")  # Example: "Welding, Roofing"
    experience = models.IntegerField(help_text="Years of experience", default=0)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='artisan_pictures/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.profession}"


class JobListing(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_listings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)  # Example: Plumbing, Carpentry
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    posted_on = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} - {self.client.username}"


class JobApplication(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='applications')
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    cover_letter = models.TextField()
    applied_on = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.artisan.username} applied for {self.job.title}"


class Transaction(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_made')
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_received')
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='transaction')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction: {self.client.username} → {self.artisan.username} (${self.amount})"


class Review(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveIntegerField(default=5, help_text="Rate from 1 to 5")
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.artisan.username} - {self.rating} stars"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - Read: {self.is_read}"

