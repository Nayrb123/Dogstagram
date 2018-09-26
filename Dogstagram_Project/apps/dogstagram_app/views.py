from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def index(request):
    return render(request, "dogstagram_app/index.html")

def createprofile(request):
    return render(request, "dogstagram_app/createprofile.html")

def processregistration(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/createprofile')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            registered = User.objects.create(first_name = request.POST['first_name'], username = request.POST['user_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashed_pw.decode())
            request.session['username'] = registered.first_name
            request.session['user_id'] = registered.id
            print(request.POST)
            return redirect('/')

def login(request):
    if request.method == 'POST':
        logged_in_user = User.objects.filter(username=request.POST['user_name']) #Get the user
        print(logged_in_user)

    if len(logged_in_user) == 0:
        messages.error(request, "No matching user!") #If it doesn't find that email in the database "No matching user!"
    elif not bcrypt.checkpw(request.POST['loginpassword'].encode(), logged_in_user[0].password.encode()):
        messages.error(request, 'Password is incorrect')
        return redirect('/createprofile')
    else:
        request.session['username'] = logged_in_user[0].first_name
        request.session['user_id'] = logged_in_user[0].id
        messages.success(request, 'Successfully Logged In!')
        return redirect('/')

def profile_page(request):
    return render(request,'dogstagram_app/profilepage.html')