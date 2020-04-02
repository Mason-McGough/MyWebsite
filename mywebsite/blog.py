import os
from datetime import datetime

from flask import Blueprint, flash, current_app, g, render_template

from mywebsite.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog')


def get_blog_post(id):
    db = get_db()
    post = db.execute(
        'SELECT * FROM post WHERE id=?',
        (id,)
    ).fetchone()
    return post

def get_blog_posts(max_posts=-1):
    db = get_db()
    posts_query = db.execute(
        'SELECT * FROM post ORDER BY date_posted DESC'
    )
    if max_posts >= 0:
        posts = posts_query.fetchmany(max_posts)
    else:
        posts = posts_query.fetchall()

    return posts

def convert_post_sqlite_to_client(post):
    return {
        'id': post['id'],
        'title': post['title'],
        'description': post['description'],
        'date_posted': post['date_posted'].strftime('%b %d, %Y'),
        'thumbnail': post['thumbnail'],
        'filename': post['filename']
    }

@bp.route('/')
def index():
    posts = get_blog_posts()
    client_posts = []
    for post in posts:
        client_posts.append(convert_post_sqlite_to_client(post))

    return render_template(
        'blog.html', 
        posts=client_posts)

@bp.route('/post/<int:id>')
def post(id):
    post = convert_post_sqlite_to_client(get_blog_post(id))
    return render_template(
        os.path.join('posts', post['filename']),
        post=post)