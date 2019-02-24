from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_url = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to="media/profile_pic", blank=True)
    def __str__(self):
        return self.user.username

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField(max_length=500)
    status = models.BooleanField(default=False)
    published_date = models.DateField(default=timezone.now)
    def __str__(self):
        return self.title
    def publish(self):
        self.status = True
        self.save()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name = "comments", on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    comment_published_date = models.DateField(default=timezone.now)
    def __str__(self):
        return self.text
    def approve(self):
        self.status=True
        self.save()
