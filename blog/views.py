from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def home(request):
    max_posts = 3
    posts = Post.objects.all()[:max_posts]
    return render(request, 'home.html', {'posts': posts, 'max_posts': max_posts})

def blog(request):
    posts = Post.objects.all()
    return render(request, 'blog.html', {'posts': posts})

def blog_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog_post.html', {'post': post})

def photos(request):
    return render(request, 'photos.html', {})
