from django.contrib import admin
from myapp.models import UserProfile,Post, Comment

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
