from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Teep
from .forms import TeepForm, SignUpForm, ProfilePicForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
# from django import forms
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated:
        form = TeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                teep = form.save(commit=False)
                teep.user = request.user
                teep.save()
                messages.success(request, ('Your Teep has been posted!'))
                return redirect('home')

        teeps = Teep.objects.all().order_by("-created_at")
        return render(request, 'home.html', {'teeps': teeps, 'form': form})
    else:
        teeps = Teep.objects.all().order_by("-created_at")
        return render(request, 'home.html', {'teeps': teeps})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, ('You must be logged in to view this page.'))
        return redirect('home')
    
def unfollow(request, pk):
    if request.user.is_authenticated:
        # get user profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow the user
        request.user.profile.follows.remove(profile)
        # Save our profile
        request.user.profile.save()
        # Return message
        messages.success(request, (f'You have successfully unfollowed {profile.user.username}.'))
        return redirect(request.META.get('HTTP_REFERER'))
        
    else:
        messages.success(request, ('You must be logged in to view this page.'))
        return redirect('home')

def follow(request, pk):
    if request.user.is_authenticated:
        # get user profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow the user
        request.user.profile.follows.add(profile)
        # Save our profile
        request.user.profile.save()
        # Return message
        messages.success(request, (f'You have successfully followed {profile.user.username}.'))
        return redirect(request.META.get('HTTP_REFERER'))
        
    else:
        messages.success(request, ('You must be logged in to view this page.'))
        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        teeps = Teep.objects.filter(user_id=pk).order_by("-created_at")

        if request.method == "POST":
            # get current user
            current_user_profile = request.user.profile
            # get form data
            action = request.POST['follow']
        
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        return render(request, 'profile.html', {'profile': profile, 'teeps': teeps})
    else:
        messages.success(request, ('You must be logged in to view this page.'))
        return redirect('home')
    
def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {'profiles': profiles})
        else:
            messages.success(request, ("That's not  your profile page..."))
        return redirect('home')
    else:
        messages.success(request, ('You must be logged in to view this page.'))
        return redirect('home')
    
def following(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'following.html', {'profiles': profiles})
        else:
            messages.success(request, ("That's not  your profile page..."))
        return redirect('home')
    else:
        messages.success(request, ('You must be logged in to view this page.'))
        return redirect('home')
    
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password= request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('WELCOME BACK! You have been logged in! Keep Teeping!'))
            return redirect('home')
        else:
            messages.error(request, ('Username or Password is incorrect! Please try again!'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('You are successfully logged out! Sorry to teep you go!'))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            # Login USER
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You have successfully registered! WELCOME!'))
            return redirect('home')
    return render(request, 'register.html', {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)

        user_form = SignUpForm(request.POST or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and  profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ('Your profile has been updated successfully.'))
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        messages.success(request, ('You Must be Logged In to Update Your Profile.'))
        return redirect('login')

def search_user(request):
    if request.method == "POST":
        search = request.POST['search']
        # Search the Database
        searched = User.objects.filter(username__contains= search)
        return render(request, 'search_user.html', {'search': search, 'searched':  searched}) 
    else:
        return render(request, 'search_user.html', {})
    
    
"""
Teep related Views start from here!
""" 
   
    
def teep_like(request, pk):
    if request.user.is_authenticated:
        teep = get_object_or_404(Teep, id=pk)
        if teep.likes.filter(id=request.user.id):
            teep.likes.remove(request.user)
        else:
            teep.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
        
    else:
        messages.success(request, ('You Must be Logged In to Update Your Profile.'))
        return redirect('login')
    
def teep_share(request, pk):
    teep = get_object_or_404(Teep, id=pk)
    if teep:
        return render(request, 'teep_share.html', {'teep': teep})
    else:
        messages.success(request, ("That teep doesn't exist..."))
        return redirect('login')
    
def teep_delete(request, pk):
    if request.user.is_authenticated:
        teep = get_object_or_404(Teep, id=pk)
        # Let's verify the owner of the teep
        if request.user.username == teep.user.username:
            # Delete teep
            teep.delete()
            messages.error(request, ('Your teep has been deleted successfully!'))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, ("Sorry, You can't delete this teep!"))
            return redirect('home')
    else:
        messages.error(request, ('Please Login to delete this teep!'))
        return redirect(request.META.get("HTTP_REFERER"))
    
def teep_edit(request, pk):
    if request.user.is_authenticated:
        teep = get_object_or_404(Teep, id=pk)
        # Let's verify the owner of the teep
        if request.user.username == teep.user.username:
            
            form = TeepForm(request.POST or None, instance=teep)
            if request.method == "POST":
                if form.is_valid():
                    teep = form.save(commit=False)
                    teep.user = request.user
                    teep.save()
                    messages.success(request, ('Your Teep has been updated Successfully!'))
                    return redirect('home')
            else:
                return render(request, 'teep_edit.html', {'form': form, 'teep': teep})
        else:
            messages.error(request, ("Sorry, You can't edit this teep!"))
            return redirect('home')
    else:
        messages.error(request, ('Please Login to delete this teep!'))
        return redirect(request.META.get("HTTP_REFERER"))
    
def teep_search(request):
    if request.method == "POST":
        search = request.POST['search']
        # Search the Database
        searched = Teep.objects.filter(body__contains= search)
        return render(request, 'search.html', {'search': search, 'searched':  searched}) 
    else:
        return render(request, 'search.html', {})