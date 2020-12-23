from django.shortcuts import render,HttpResponseRedirect
from .forms import UserSignUpForm,UserLoginForm,AddPost,EditProfileForm,ChangePassForm
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib import messages
from .models import Post
from django.contrib.auth.models import Group


def home_view(request):
    return render(request,'home.html')

def dashboard(request):
   if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user.username

        return render(request,'dashboard.html',{'posts': posts,'name':user})
   else:
       return HttpResponseRedirect('/login/')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def log_in(request):
    if not request.user.is_authenticated:
            if request.method == 'POST':
                lg = UserLoginForm(request=request,data=request.POST)
                if lg.is_valid():
                    uname = lg.cleaned_data['username']
                    upass = lg.cleaned_data['password']

                    user = authenticate(username = uname, password = upass)

                    if user is not None:
                        login(request,user)
                        messages.success(request,'Login Succesfully ')
                        return HttpResponseRedirect('/dashboard/')
            else:
                lg = UserLoginForm()
            return render(request,'login.html',{'form': lg})
    else:
        return HttpResponseRedirect('/')

def sign_up(request):
    if not request.user.is_authenticated:
            if request.method == 'POST':
                su = UserSignUpForm(request.POST)
                if su.is_valid():
                    messages.success(request,'Your Account has been created .')
                    su.save()
                    user = su.save()
                    group = Group.objects.get(name = 'Author')
                    user.groups.add(group)
                    su = UserSignUpForm()
            else:
                su = UserSignUpForm()
            return render(request,'signin.html', {'form' : su })
    else:
        return HttpResponseRedirect ('/')


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            ap = AddPost(request.POST)
            if ap.is_valid():
                title = ap.cleaned_data['title']
                desc = ap.cleaned_data['desc']
                post = Post(title=title, desc=desc)
                post.save()
                messages.success(request,'Your post is now available in Dashboard .')
                return HttpResponseRedirect('/dashboard/')
        else:
            ap = AddPost()
        return render(request,'addpost.html',{'form': ap })
    else:
        return HttpResponseRedirect('/login/')


def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            up = Post.objects.get(pk=id)
            update = AddPost(request.POST,instance=up)
            if update.is_valid():
                update.save()
                return HttpResponseRedirect('/dashboard/')

        else:
            up = Post.objects.get(pk=id)
            update = AddPost(instance=up)

    return render(request,'updatepost.html',{'form': update})

def delete_post(request,id):
    if request.user.is_authenticated:
            if request.method == 'POST':
                dp = Post.objects.get(pk = id)
                dp.delete()
                return HttpResponseRedirect('/dashboard/')


def user_profileee(request):
    if request.user.is_authenticated:
        uname = request.user.username
        fname = request.user.first_name
        lname = request.user.last_name
        email = request.user.email
        return render(request,'userprofile.html',{'uname': uname,'fname': fname,'lname': lname,'email':email})
    else:
        return HttpResponseRedirect('/login/')
def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            sp = EditProfileForm(request.POST,instance=request.user)
            if sp.is_valid():
                sp.save()
                messages.success(request,'Your profile is Update .')
                return HttpResponseRedirect('/userprofile/')
        else:
            sp = EditProfileForm(instance=request.user)
        return render(request,'editprofile.html',{'form': sp})
    else:
        return HttpResponseRedirect('/login/')

def change_password(request):
    if request.method == 'POST':
        cp = ChangePassForm(user=request.user,data=request.POST)
        if cp.is_valid():
            cp.save()
            update_session_auth_hash(request,cp.user)
            messages.success(request, 'Your password is Changed .')
            return HttpResponseRedirect('/cpass/')

    else:
        cp = ChangePassForm(user=request.user)
    return render(request,'cpass.html',{'form': cp})