import os

from flask import Blueprint, flash, current_app, g, render_template

bp = Blueprint('blog', __name__, url_prefix='/blog')


def get_blog_posts():
    if 'blog_posts' not in g:
        g.blog_posts = [
            {
                'id': 0,
                'title': 'Welcome',
                'description': 'An introduction to the creation of this website',
                'date_posted': 'Feb. 17, 2018',
                'thumbnail': 'welcome.jpg',
                'filename': 'welcome.html'
            }
        ]

    return g.blog_posts

@bp.route('/')
def index():
    return render_template('blog.html', posts=get_blog_posts())

@bp.route('/post/<int:id>')
def post(id):
    post = get_blog_posts()[id]
    return render_template(os.path.join('posts', post['filename']))