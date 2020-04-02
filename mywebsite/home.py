from flask import Blueprint, flash, current_app, g, render_template

from .blog import get_blog_posts, convert_post_sqlite_to_client

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    posts = get_blog_posts(max_posts=3)
    client_posts = []
    for post in posts:
        client_posts.append(convert_post_sqlite_to_client(post))
    
    return render_template(
        'home.html', 
        posts=client_posts)