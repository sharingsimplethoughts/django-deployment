from django import forms
from myapp.models import UserProfile,Post,Comment

from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_url','profile_pic',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','text',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
