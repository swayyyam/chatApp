from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ChatMessage
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_user
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        login_user(request, user)  
        return redirect('homepage')  
    return render(request, 'chat/signup.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_user(request, user)
            return redirect('homepage') 
            
    return render(request, 'chat/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def homepage(request):
    return render(request, 'chat/homepage.html')

@login_required(login_url='login')
def chatPage(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    users = User.objects.exclude(id=request.user.id)  
    context = {"users": users}
    return render(request, "chat/chatPage.html", context)

@login_required
def get_messages(request, username):
    recipient = User.objects.get(username=username)
    messages = ChatMessage.objects.filter(
        (Q(user=request.user) & Q(recipient=recipient) & ~Q(deleted_by_user=True)) |
        (Q(user=recipient) & Q(recipient=request.user) & ~Q(deleted_by_recipient=True))
    ).order_by("timestamp")
    return JsonResponse([
        {"sender": msg.user.username, "message": msg.message}
        for msg in messages
    ], safe=False)

@login_required
def delete_chat(request, username):
    if request.method == "DELETE":
        recipient = get_object_or_404(User, username=username)
        updated_count = ChatMessage.objects.filter(
            user=request.user, recipient=recipient
        ).update(deleted_by_user=True)
        updated_count += ChatMessage.objects.filter(
            user=recipient, recipient=request.user
        ).update(deleted_by_recipient=True)
        if updated_count > 0:
            return JsonResponse({"message": "Messages deleted successfully."}, status=200)
        else:
            return JsonResponse({"message": "No messages found to delete."}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)




