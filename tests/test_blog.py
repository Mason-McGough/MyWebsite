import pytest


class TestBlog:
    def test_blog(self, client):
        response = client.get('/blog/')
        assert response.status_code == 200
        assert b"Welcome" in response.data

    def test_blog_post(self, client):
        response = client.get('/blog/post/1')
        assert response.status_code == 200
        assert b"Welcome" in response.data
