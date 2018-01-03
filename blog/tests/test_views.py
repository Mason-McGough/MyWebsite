from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from ..views import home, blog, blog_post
from ..models import Post

class HomeTests(TestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_contains_link_to_blog_page(self):
        blog_url = reverse('blog')
        self.assertContains(self.response, f'href="{blog_url}"')

class BlogTests(TestCase):
    def setUp(self):
        url = reverse('blog')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_view(self):
        view = resolve('/blog/')
        self.assertEquals(view.func, blog)

class BlogPostTests(TestCase):
    def setUp(self):
        Post.objects.create(title='Sample Title', description='Sample description.')

    def test_status_code(self):
        url = reverse('blog_post', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_not_found_status_code(self):
        url = reverse('blog_post', kwargs={'pk': 256})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_url_resolves_view(self):
        view = resolve('/blog/1/')
        self.assertEquals(view.func, blog_post)