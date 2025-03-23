import os
from django.shortcuts import render,redirect
from .forms import DocumentUploadForm
from .models import Document, Prompt
import google.generativeai as genai  # Gemini AI
from django.contrib.auth import authenticate, login, logout

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
# Set up Google API Key
import google.generativeai as genai  # Gemini AI

# Configure Google API Key using Django settings
genai.configure(api_key=settings.GOOGLE_API_KEY)


def home(request):
    return render(request, "home.html")
def upload_document(request):
    response_text = None  
    recent_prompts = Prompt.objects.all().order_by('-created_at')[:5]  

    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        user_prompt = request.POST.get("prompt", "").strip()  # Get prompt from user input

        if form.is_valid() and user_prompt:
            document = form.save()
            file_path = document.file.path  

            try:
                # Upload file to Gemini AI
                with open(file_path, "rb") as f:
                    uploaded_file = genai.upload_file(f, mime_type="application/pdf")

                # Initialize model
                model = genai.GenerativeModel("gemini-1.5-flash")

                # Generate response using user-provided prompt
                response = model.generate_content([uploaded_file, user_prompt])

                # Extract response text
                response_text = response.text if hasattr(response, "text") else "No response received."

                # Save prompt & response
                Prompt.objects.create(text=user_prompt, response=response_text)

            except Exception as e:
                response_text = f"Error generating response: {str(e)}"

    else:
        form = DocumentUploadForm()

    return render(request, "upload.html", {"form": form, "response_text": response_text, "recent_prompts": recent_prompts})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('upload')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if all fields are filled
        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required")
            return redirect('register')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        # Check if email is already used
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return redirect('register')

        # Create and save the user
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')

    return render(request, 'register.html')
from django.shortcuts import render, redirect
from .models import Case
from .forms import CaseForm
from django.http import JsonResponse

def case_list(request):
    cases = Case.objects.filter(user=request.user)
    return render(request, "case_list.html", {"cases": cases})

def add_case(request):
    if request.method == "POST":
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.user = request.user
            case.save()
            return redirect("case_list")
    else:
        form = CaseForm()
    return render(request, "add_case.html", {"form": form})

def get_cases(request):
    cases = Case.objects.filter(user=request.user).values("title", "description", "date")
    return JsonResponse(list(cases), safe=False)
from django.shortcuts import render
from .models import Case

def upload_view(request):
    cases = Case.objects.all()
    return render(request, "upload.html", {"cases": cases})
