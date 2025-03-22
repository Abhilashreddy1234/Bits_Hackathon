import os
from django.shortcuts import render,redirect
from .forms import DocumentUploadForm
from .models import Document, Prompt
import google.generativeai as genai  # Gemini AI
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from django.contrib import messages
# Set up Google API Key
genai.configure(api_key="AIzaSyDDK-Vaaf9V0gYabJVYoPMfX2oRBV86BkU")

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

def user_register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully")
            return redirect('login')
    return render(request, 'register.html')