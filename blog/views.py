from django.shortcuts import render
from .models import Post

# Create your views here.
def home(requests):
    posts = Post.objects.all()
    return render(requests, 'home.html', {'posts': posts})