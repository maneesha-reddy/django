from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('post/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'), 
    path('signup/', views.signup, name='signup'),
    path('',views.home,name='home'),
    path('profile/',views.update_profile,name='update_profile'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name= "blog/login.html"), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name= "blog/logged_out.html"), name='logout'),
    #url(r'^logout/$', auth_views.LogoutView, {'template_name': 'blog/logged_out.html'}, name='logout'),
    
]




