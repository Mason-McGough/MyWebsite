from flask import Blueprint, flash, current_app, g, render_template

from .blog import get_blog_posts

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    return render_template(
        'home.html', 
        posts=get_blog_posts(max_posts=3))