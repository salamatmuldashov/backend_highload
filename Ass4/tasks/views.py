import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .forms import CustomUserCreationForm
from .task import send_email_task, process_dataset
from .models import Website, Dataset
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import WebsiteSerializer, DatasetSerializer
from .permissions import IsAdminUser
from django.views.generic import DetailView




def home(request):
    context = {
        'user': request.user,  
        'message': 'Welcome to the Home Page!'
    }
    return render(request, 'home.html', context)


@csrf_exempt
def send_email_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            recipient = data.get('recipient')
            subject = data.get('subject')
            body = data.get('body')
            print(recipient)
            send_email_task.delay(recipient, subject, body)
            return JsonResponse({'message': 'Email queued successfully!'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please check your details.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Generate OTP (One-Time Password) and send it to the user's email
            otp = get_random_string(length=6, allowed_chars='0123456789')
            request.session['otp'] = otp
            request.session['user_id'] = user.id

            # Send OTP to the user's email
            send_mail(
                'Your OTP for Login',
                f'Your One-Time Password (OTP) is: {otp}',
                'no-reply@yourdomain.com',  # From email address
                [user.email],  # To user email
                fail_silently=False,
            )

            # Redirect to OTP verification page
            return redirect('verify_otp')

        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        session_otp = request.session.get('otp')
        user_id = request.session.get('user_id')
        print(request.session.get('otp'))
        if otp == session_otp:
            user = User.objects.get(id=user_id) 
            auth_login(request, user)  
            del request.session['otp'] 
            del request.session['user_id']
            return redirect('home')  
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, '2fa.html')

class WebsiteListCreate(generics.ListCreateAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

   

class WebsiteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = [permissions.IsAuthenticated]


class DatasetUploadView(generics.CreateAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    def perform_create(self, serializer):
        dataset = serializer.save(status='pending')

        process_dataset.delay(dataset.id)

class DatasetListView(generics.ListAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

class DatasetProgressView(generics.RetrieveAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        dataset = self.get_object()

        # If needed, you can serialize the data for API usage (JSON response)
        # serializer = self.get_serializer(dataset)

        # Render the template and pass the dataset context to it
        return render(request, 'progress.html', {'dataset': dataset})