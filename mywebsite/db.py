import os, sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    # g is an object for storing data for a request
    if 'db' not in g:
        g.db = sqlite3.connect(
            # current_app is a ref to the app
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def execute_sqlite_script(script):
    db = get_db()
    with current_app.open_resource(os.path.join('sql', script)) as f:
        db.executescript(f.read().decode('utf8'))

def init_db():
    execute_sqlite_script('post.sql')

def insert_post(title, description, date_posted, thumbnail, filename):
    """Insert row into post table."""
    db = get_db()
    db.execute(
        'INSERT INTO post (title, description, date_posted, thumbnail, filename)'
        'VALUES (?, ?, ?, ?, ?)',
        (title, description, date_posted, thumbnail, filename)
    )
    db.commit()

def get_post(id):
    """Get row from post table with given ID."""
    db = get_db()
    post = db.execute(
        'SELECT * FROM post WHERE id=?',
        (id,)
    ).fetchone()
    return post

def get_posts():
    """Retrieve all rows of post table."""
    db = get_db()
    rows = db.execute('SELECT * FROM post').fetchall()
    return rows

def delete_post(id):
    """Delete post with given ID."""
    db = get_db()
    db.execute(
        'DELETE FROM post WHERE id=?',
        (id,)
    )
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('insert-post')
@click.option('--title', prompt='Post title', help='The title of the post.')
@click.option('--description', prompt='Description', help='The description of the post.')
@click.option('--date_posted', prompt='Date', help='The date of original post.')
@click.option('--thumbnail', prompt='Path to thumbnail (from /static/images/blog)', help='The path to the thumbnail image.')
@click.option('--filename', prompt='HTML filename (from /templates/posts)', help='The filename of the HTML file template.')
@with_appcontext
def insert_post_command(title, description, date_posted, thumbnail, filename):
    insert_post(title, description, date_posted, thumbnail, filename)
    response = \
        'Inserted post:\n' \
        '\ttitle: {}\n' \
        '\tdescription: {}\n' \
        '\tdate_posted: {}\n' \
        '\tthumbnail: {}\n' \
        '\tfilename: {}'\
        .format(title, description, date_posted, thumbnail, filename)
    click.echo(response)

@click.command('get-post')
@click.option('--id', prompt='Post ID', help='The ID of the post to get.')
@with_appcontext
def get_post_command(id):
    post = get_post(id)

    response = \
        'Retrieved post {}:\n' \
        '\ttitle: {}\n' \
        '\tdescription: {}\n' \
        '\tdate_posted: {}\n' \
        '\tthumbnail: {}\n' \
        '\tfilename: {}'\
        .format(
            id,
            post['title'], 
            post['description'], 
            post['date_posted'], 
            post['thumbnail'], 
            post['filename'])
    click.echo(response)

@click.command('get-posts')
@with_appcontext
def get_posts_command():
    rows = get_posts()
    for row in rows:
        click.echo('Post: {}'.format(row['id']))
        for key in row.keys():
            click.echo('\t{}: {}'.format(key, row[key]))

@click.command('delete-post')
@click.option('--id', prompt='Post ID', help='The ID of the post to delete.')
@with_appcontext
def delete_post_command(id):
    post = get_post(id)

    click.echo('Post: {}'.format(id))
    for key in post.keys():
        click.echo('\t{}: {}'.format(key, post[key]))
    if click.confirm('Delete?', abort=True):
        delete_post(id)
        click.echo('Deleted post with ID: {}'.format(id))


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(insert_post_command)
    app.cli.add_command(get_post_command)
    app.cli.add_command(get_posts_command)
    app.cli.add_command(delete_post_command)
    