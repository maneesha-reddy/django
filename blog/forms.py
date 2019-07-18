from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .models import Profile
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,required=True )
    last_name = forms.CharField(max_length=30,required=True)
    email = forms.EmailField(max_length=30,required=True)
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email','password1','password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location','birth_date',)

