from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def index(request):
    if 'user_id' not in request.session:
        return redirect('/createprofile')
    else:
        user = {
            "user": User.objects.get(id = request.session['user_id'])
        }
        return render(request, "dogstagram_app/index.html", user)

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
        return redirect('/')

def profile_page(request, id):
    if 'user_id' not in request.session:
        return redirect('/createprofile')
    else:
        user = {
            "user": User.objects.get(id = request.session['user_id'])
        }
        return render(request,'dogstagram_app/profilepage.html', user)

def editpage(request, id):
    if 'user_id' not in request.session:
        return redirect('/createprofile')
    else:
        user = {
            "user": User.objects.get(id=id)
        }
        return render(request, 'dogstagram_app/editprofile.html', user)

def processedit(request, id):
    if request.method == 'POST':
        if len(request.POST['edituser_name']) > 15:
            messages.error(request, "Username can't be more than 15 characters.")
        if len(request.POST['edituser_name']) < 1:
            messages.error(request, "Please enter a username.")
        if len(request.POST['editfirst_name']) < 1:
            messages.error(request, "Please enter a first name.")
        if len(request.POST['editlast_name']) < 1:
            messages.error(request, "Please enter a last name")
        if len(request.POST['edit_bio']) > 140:
            messages.error(request, "Bio can not exceed 140 characters.")
            return redirect(f'/editprofile/{id}')
        
        else:
            user = User.objects.get(id = id)
            user.username = request.POST['edituser_name']
            user.first_name = request.POST['editfirst_name']
            user.last_name = request.POST['editlast_name']
            user.bio = request.POST['edit_bio']
            user.save()
            return redirect(f'/profilepage/{id}')