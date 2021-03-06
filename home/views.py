from django.shortcuts import render
from django.shortcuts import HttpResponse,redirect
from .models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
from django.db.models import Avg, Max,Count

# Create your views here.
# HTML Pages

def home(request):
    #Fetch top three posts based on no of views.
    top_post = Post.objects.annotate(no_of_views=Count('views')).order_by('no_of_views')[:3]
    # top_post = Post.objects.filter(views=1)

    context = {"top_post":top_post}
    # messages.success(request, 'Welcome to HOME')
    return render(request, 'home/home.html',context)

def about(request):

    messages.warning(request, 'Welcome to ABOUT')
    return render(request,'home/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        content = request.POST.get('content', '')
        print(name,email,phone,content)
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, 'Please fill the form correctly')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request,'Your message has been sent successfully')
    return render(request,'home/contact.html')

def search(request):
    query =request.GET['query']
    if len(query)>50:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning(request, 'Please fill the form correctly! No Search Results')

    params = {"allPosts":allPosts,'query':query}
    return render(request,'home/search.html',params)

#Authentications API

def handleSignup(request):
    if request.method == "POST":
        #Get the parameter
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #CHECK FOR ERRORNEOUS INPUT
        if not username.isalnum():
            messages.error(request, 'Username should be number and characters')
            return redirect('home')
        if pass1 != pass2:
            messages.error(request,'Password do not match')
            return redirect('home')

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your account successfully created')
        return redirect('home')


    else:
        return HttpResponse("404 - Page not found")

def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        logipassword = request.POST['loginpass']

        user = authenticate(username = loginusername,password = logipassword)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentical,Please try again")
            
    return HttpResponse("404 - page not found")

def handleLogout(request):
    logout(request)
    messages.success(request, "Succeessfully Logout")
    return redirect('home')

        

