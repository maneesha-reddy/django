from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Profile
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .forms import UserForm
from .forms import ProfileForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from .filters import PostFilter
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth import  get_user_model
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseNotFound
User = get_user_model()

@login_required(login_url='/')
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile was successfully updated!')
            return redirect('update_profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'blog/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def home(request):
    posts=Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})


def signup(request):
    posts=Post.objects.all()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #print(user.pk)
            login(request, user)
            return render(request,'blog/home.html',{'posts':posts})
            
    else:
        form = UserForm()
    return render(request, 'blog/signup.html', {'form': form})

@login_required(login_url='/login/')
def post_detail(request,pk):
    Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk) 
    return render(request, 'blog/post_detail.html', {'post': post})  
    
@login_required(login_url='/login/')
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required(login_url='/login/')
def post_edit(request, pk):
     post = get_object_or_404(Post, pk=pk)
     if request.method == "POST":
         form = PostForm(request.POST, instance=post)
         if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
     else:
         form = PostForm(instance=post)
     return render(request, 'blog/post_edit.html', {'form': form})




#@require_http_methods(["POST"])

#@csrf_protect


@login_required(login_url='/login/')
def post_list(request):
  a=request.user.is_authenticated
  print(a)
  
  if request.user.is_authenticated:
  #if current_user.is_authenticated:   
        user_list=Post.objects.all()
        superusers = User.objects.filter(is_superuser=True)
        if request.user not in superusers:
           s=Post.objects.filter(Q(author= request.user))
           user_list=s
        else:
           user_list=Post.objects.all()
    
    
        if "title" in request.GET:
           title = request.GET.get('title', None)
           #print(title)
           title_list = title.split(' ')
           q =s.filter(Q(title__icontains=title)|Q(text__icontains=title))
           user_list=q


    
        page = request.GET.get('page', 1)
        paginator = Paginator(user_list, 2)
        print(paginator)
        try:
            posts = paginator.page(page)
            #print(posts)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(request, 'blog/post_list.html',{'posts': posts})
  else:
    print("hii")
    return HttpResponseNotFound("hello") 

