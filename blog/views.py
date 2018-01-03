from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def home(request):
    return render(request, 'home.html')

def blog(request):
    posts = Post.objects.all()
    return render(request, 'blog.html', {'posts': posts})

def blog_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog_post.html', {'post': post})