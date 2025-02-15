from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from .permissions import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.core.validators import validate_email

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])  # Anyone can register
def register_user(request):
    data = JSONParser().parse(request)

    if User.objects.filter(username=data['username']).exists():
        return JsonResponse({'error': 'Username already taken'}, status=400)

    if User.objects.filter(email=data.get('email', '')).exists():
        return JsonResponse({'error': 'Email already in use'}, status=400)

    try:
        validate_email(data.get('email', ''))
    except ValidationError:
        return JsonResponse({'error': 'Invalid email format'}, status=400)

    try:
        validate_password(data['password'])
    except ValidationError as e:
        return JsonResponse({'error': e.messages}, status=400)

    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        user_type=data.get('user_type', 'client'),
        phone_number=data.get('phone_number', ''),
        location=data.get('location', '')
    )

    serializer = UserSerializer(user)
    return JsonResponse(serializer.data, status=201)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])  # Anyone can log in
def login_user(request):
    data = JSONParser().parse(request)
    user = authenticate(username=data['username'], password=data['password'])
    
    if user is not None:
        login(request, user)  # Django session-based login
        return JsonResponse({'message': 'Login successful', 'user': UserSerializer(user).data})
    
    return JsonResponse({'error': 'Invalid credentials'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    serializer = UserSerializer(request.user)
    return JsonResponse(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow anyone to register
def user_list_create(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['password'] = make_password(data['password'])  # Hash password
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)

    # Allow GET requests to anyone, but restrict updates/deletions to the user themselves
    if request.method in ['PUT', 'DELETE'] and not IsOwner().has_object_permission(request, None, user):
        return JsonResponse({'error': 'You can only edit or delete your own profile'}, status=403)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=204)



@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def artisan_profile(request, pk):
    profile = get_object_or_404(ArtisanProfile, pk=pk)

    if request.method == 'GET':
        serializer = ArtisanProfileSerializer(profile)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArtisanProfileSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Authenticated users can view jobs
def job_list_create(request):
    if request.method == 'GET':
        jobs = JobListing.objects.all()
        serializer = JobListingSerializer(jobs, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        if not IsClient().has_permission(request, None):  # Check if user is a client
            return JsonResponse({'error': 'Only clients can post jobs'}, status=403)

        data = JSONParser().parse(request)
        data['client'] = request.user.id  # Assign job to logged-in client
        serializer = JobListingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def job_detail(request, pk):
    job = get_object_or_404(JobListing, pk=pk)

    if request.method == 'GET':
        serializer = JobListingSerializer(job)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = JobListingSerializer(job, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        job.delete()
        return JsonResponse({'message': 'Job deleted successfully'}, status=204)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Authenticated users can view applications
def job_application_list_create(request):
    if request.method == 'GET':
        applications = JobApplication.objects.all()
        serializer = JobApplicationSerializer(applications, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        if not IsArtisan().has_permission(request, None):  # Check if user is an artisan
            return JsonResponse({'error': 'Only artisans can apply for jobs'}, status=403)

        data = JSONParser().parse(request)
        data['artisan'] = request.user.id  # Assign artisan as the applicant
        serializer = JobApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def transaction_list_create(request):
    if request.method == 'GET':
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def review_list_create(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    serializer = NotificationSerializer(notifications, many=True)
    return JsonResponse(serializer.data, safe=False)

