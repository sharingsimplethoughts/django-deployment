from myapp.models import UserProfile,Post,Comment
from myapp.forms import UserForm, UserProfileForm, PostForm, CommentForm

from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Home(ListView):
    model = Post
    fields = ('author','title','published_date')
    template_name = 'myapp/home.html'
    def get_queryset(self):
        return Post.objects.filter(status=True).order_by('published_date')

class About(View):
    def get(self,request):
        return render(request,'myapp/about.html')

def register(request):
    userform = UserForm()
    userprofileform = UserProfileForm()
    registered=False
    if request.method == 'POST':
        userform = UserForm(data=request.POST)
        userprofileform = UserProfileForm(data = request.POST)
        if userform.is_valid() and userprofileform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()

            userprofile = userprofileform.save(commit=False)
            userprofile.user = user
            if 'profile_pic' in request.FILES:
                userprofile.profile_pic = request.FILES['profile_pic']
            userprofile.save()
            registered = True
        else:
            print(userform.errors, userprofileform.errors)

    return render(request,'myapp/register.html',{'registered':registered,'userform':userform,'userprofileform':userprofileform})

def loginview(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("This user is not active. Contact admin")
        else:
            return HttpResponse("ID or Pass incorrect")
    return render(request, "myapp/login.html")

@login_required
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))

# class NewPost(CreateView):
#     model = Post
#     fields = ('author','title','text')
#     template_name="myapp/newpost.html"
#     success_url = reverse_lazy("home")
@login_required
def newpost(request,pk):
    u = get_object_or_404(User,pk=pk)
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.author = u
            form.save()
            return redirect("home")
    return render(request,'myapp/newpost.html',{'form':form})


class DraftPost(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Post
    fields = ('title','text','published_date')
    template_name="myapp/draft.html"
    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(status=False, author=user)

class PostDetail(DetailView):
    context_object_name = "postdetail"
    model =Post
    fields = ('author','title','text')
    template_name = "myapp/postdetail.html"

@login_required
def publishview(request,pk):
    w = get_object_or_404(Post, pk=pk)
    w.publish()
    return redirect('home')

class EditView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = Post
    fields = ('title','text')
    template_name = "myapp/newpost.html"
    success_url = reverse_lazy("home")

class DeletingView(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    model = Post
    success_url = reverse_lazy("home")

@login_required
def addcomment(request,pk):
    a = get_object_or_404(Post,pk=pk)
    u = request.user
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            com = form.save(commit = False)
            com.post = a
            com.author = u
            com.save()
            return redirect('myapp:detail',pk=a.pk)
    return render(request,'myapp/comment.html',{'form':form})

@login_required
def approvecom(request,pk):
    com = get_object_or_404(Comment,pk=pk)
    com.approve()
    return redirect("myapp:detail",pk=com.post.pk)

@login_required
def deletecom(request,pk):
    com = get_object_or_404(Comment,pk=pk)
    temp = com.post.pk
    com.delete()
    return redirect('myapp:detail',pk=temp)
