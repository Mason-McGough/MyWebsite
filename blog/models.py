from django.db import models
from django import template
from django.template.loader import render_to_string
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=64, unique=True)
    filename = models.CharField(max_length=64)
    date_posted = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=128)

    class Meta:
        ordering = ['-date_posted']

    def get_html(self):
        try:
            return render_to_string(self.filename)
        except template.TemplateDoesNotExist:
            return render_to_string('not-found.html')

class Comment(models.Model):
    content = models.CharField(max_length=255)
    date_posted = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name='comments')
    commentor = models.ForeignKey(User, related_name='comments')