from django.shortcuts import render
from .models import Post

# Create your views here.
def home(requests):
    return render(requests, 'home.html')

def blog(requests):
    posts = Post.objects.all()
    return render(requests, 'blog.html', {'posts': posts})
