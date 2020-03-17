import os

from flask import Blueprint, flash, current_app, g, render_template

BLOG_POSTS = [
    {
        'id': 0,
        'title': 'Multivariable Calculus with Python',
        'description': 'A review of fundamental multivariable calculus concepts with Python and Jupyter notebooks',
        'date_posted': 'Aug. 21, 2018',
        'thumbnail': 'laplacian-of-f.png',
        'filename': 'multivariable-calculus.html'
    },
    {
        'id': 1,
        'title': 'Operations Graph',
        'description': 'A method for running function operations in sequence with piped outputs',
        'date_posted': 'May 7, 2018',
        'thumbnail': 'ops-graph-thumb.png',
        'filename': 'operations-graph.html'
    },
    {
        'id': 2,
        'title': 'Setting Up This Server',
        'description': 'How and why I created the server running this website',
        'date_posted': 'Feb. 25, 2018',
        'thumbnail': 'setting-up-this-server.png',
        'filename': 'setting-up-this-server.html'
    },
    {
        'id': 3,
        'title': 'Welcome',
        'description': 'An introduction to the creation of this website',
        'date_posted': 'Feb. 17, 2018',
        'thumbnail': 'welcome.jpg',
        'filename': 'welcome.html'
    }
]

bp = Blueprint('blog', __name__, url_prefix='/blog')


def get_blog_posts(max_posts=-1):
    if 'blog_posts' not in g:
        g.blog_posts = BLOG_POSTS

    if max_posts < 0:
        blog_posts = g.blog_posts
    else:
        blog_posts = g.blog_posts[:max_posts]

    return blog_posts

@bp.route('/')
def index():
    return render_template('blog.html', posts=get_blog_posts())

@bp.route('/post/<int:id>')
def post(id):
    post = get_blog_posts()[id]
    return render_template(
        os.path.join('posts', post['filename']),
        post=post)