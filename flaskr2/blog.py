from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,current_app,get_flashed_messages,session
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os
from oauth2.auth import login_required
from oauth2.db import get_db

#import json
from datetime import datetime
from datetime import timedelta

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
bp = Blueprint('blog', __name__)

#@bp.route('/')
@bp.route('/',defaults={"page": 1})
@bp.route('/<int:page>')
def index(page):
    print(page,'id')
    posts=get_all_posts()
    tags=['football','rap','movies']
    args = request.args 
    #print(args)
    #print(args.getlist('filter_page'))
    #print(args.get("tag"),'tag')#for get request
    #print(args.get("filtered_posts"),'filtered_posts')
    if args.get("tag"):
        filter_posts_by_tag=[]
        for post in posts:
            if args.get("tag")==post['tag']:
                filter_posts_by_tag.append(post)
        posts=filter_posts_by_tag
    elif args.get("filter_page"):
        args = request.args 
        #print(args.get("filter_page"),'filter_page')#for get request
        filter_by=args.get("filter_page")
        filter_posts_by_title=[]
        for post in posts:
        #print(post['title'].startswith(filter_by),post['title'])
            if post['title'].startswith(filter_by):
                filter_posts_by_title.append(post)
        posts=filter_posts_by_title 
    
    amount_posts=len(posts)
    #display 5 post per page
    posts=display_per_page(posts,page,5) 
    

    
    return render_template('blog/index.html', posts=posts,tags=tags,
                            amount_posts=amount_posts,tag_selected=args.get("tag"),name_selected=args.get("filter_page"),last_feeds=['No updates'])

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    tags=['football','rap','movies']
    print('??')
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tag = request.form['tag']
        #print(title,body,tag)
        error = None
        thumbnail=upload_file()

        if not title:
            error = 'Title is required.'
        
        elif tag not in tags:
            error = 'illegal tag.'
        
        if error is not None:
            flash(error)
        elif thumbnail:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, tag,thumbnail)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, body, g.user['id'], tag,thumbnail)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username,likes,dislikes,tag'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    tags=['football','rap','movies']
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        #body=markdown.markdown_post(body)#TEST!!!!!!
        
        print(body,'??')
        tag = request.form['tag']
        error = None
        thumbnail=upload_file()

        if not title:
            error = 'Title is required.'
        elif tag not in tags:
            error = 'illegal tag.'
            
        if error is not None:
            flash(error)
        elif thumbnail:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?,tag = ?,thumbnail = ?'
                ' WHERE id = ?',
                (title, body, tag,thumbnail,id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    
    print(post['body'],'?')
    #body=markdown.reverse_markdown_post(post['body'])
    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

#delete all my posts of user 'id'
@bp.route('/<int:author_id>//delete_all', methods=('GET',))
@login_required
def delete_all(author_id):
    db = get_db()
    db.execute('DELETE FROM post WHERE author_id = ?', (author_id,))
    db.commit()
    return redirect(url_for('blog.index'))

    
    
@bp.route('/delete_comment/<int:id>', methods=('POST',))
@login_required
def delete_comment(id):
    comment=get_comment(id)
    post_id=comment['post_id']
    db = get_db()
    db.execute('DELETE FROM comment WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.show_post',id=post_id))
    
    
@bp.route('/update_comment/<int:id>', methods=('GET', 'POST'))
@login_required
def update_comment(id):
    comment=get_comment(id)
    if request.method == 'POST':
        body = request.form['body']
        #body=request.form.get('body')
        #print(body.text)
        db = get_db()
        current=db.execute(
            "SELECT datetime('now', 'localtime')"
        ).fetchone()
        #print(current[0])
        #print(type(current['datetime']))
        db.execute(
            'UPDATE comment SET body = ?,created = ? '
            ' WHERE id = ?',
            (body,current[0] ,id)
        )
        db.commit()
        return redirect(url_for('blog.show_post',id=comment['post_id'])) #need to think update time
        #return render_template('blog/show.html', id=comment['post_id'])
    return render_template('blog/edit_comment.html', comment=comment)



    
@bp.route('/post/<int:id>', methods=('GET', 'POST'))
@login_required
def show_post(id):
    my_post=get_post(id,False)
    comments=get_comments(id)
    publishers=[]
    comments_actual_time=[]
    for comment in comments:
            #print(type(comment['created']),comment['created'])
            publisher_name=get_name_publisher(comment['publisher_id'])
            publishers.append(publisher_name['username']) #2022-12-25 22:03:23
            #comments_actual_time.append(comment['created']+timedelta(hours=2))
            comments_actual_time.append(datetime.strptime(comment['created'],'%Y-%m-%d %H:%M:%S'))
    #print(comments_actual_time[0])
    #print(len(publishers))
    if request.method == 'POST':
        opi = request.get_data().decode("utf-8").split('=')[1] 
        #print(opi)
        if opi == 'Like':
           update_like(id,my_post,g.user['id'])
        elif opi == 'Dislike':
           update_dislike(id,my_post,g.user['id']) 
        else:
           opi=opi.replace('+',' ')
           print(opi)
           add_comment(id, g.user['id'], opi)
    user_new=get_like_dislike_post()  
    
    body=markdown.markdown(my_post['body'])
    #print(body)
    body=bleach.clean(body)
    print(body)
    return render_template(
                            'blog/show.html',post=my_post,body=body,user=user_new,
                            comments_post=comments,comment_publishers=publishers,
                            comment_times=comments_actual_time) #work!!! 3


def update_like(id,my_post,user):
         db = get_db()
         if '('+str(id)+')' not in g.user['liked_posts']:
             if '('+str(id)+')' not in g.user['disliked_posts']:
                 db.execute(
                     'UPDATE post SET likes=?'
                     ' WHERE id = ?',
                     (my_post['likes']+1,id)
                     )
                 db.execute(
                     'UPDATE user SET liked_posts=?'
                     ' WHERE id = ?',
                     (g.user['liked_posts']+' ('+str(id)+')',user)
                     )         
         else:
             db.execute(
                 'UPDATE post SET likes=?'
                 ' WHERE id = ?',
                 (my_post['likes']-1,id)
                 )
             list_of_liked_posts=g.user['liked_posts'].split(' ')
             list_of_liked_posts.remove('('+str(id)+')')
             str_liked_post=" ".join(list_of_liked_posts)
             db.execute(
                 'UPDATE user SET liked_posts=?'
                 ' WHERE id = ?',
                 (str_liked_post,user)
                 )
         db.commit()

def update_dislike(id,my_post,user):
         db = get_db()
         if '('+str(id)+')' not in g.user['disliked_posts']:
             if '('+str(id)+')' not in g.user['liked_posts']:
                 db.execute(
                     'UPDATE post SET dislikes=?'
                     ' WHERE id = ?',
                     (my_post['dislikes']+1,id)
                     )
                 db.execute(
                     'UPDATE user SET disliked_posts=?'
                     ' WHERE id = ?',
                     (g.user['disliked_posts']+' ('+str(id)+')',user)
                     )         
         else:
             db.execute(
                 'UPDATE post SET dislikes=?'
                 ' WHERE id = ?',
                 (my_post['dislikes']-1,id)
                 )
             list_of_disliked_posts=g.user['disliked_posts'].split(' ')
             list_of_disliked_posts.remove('('+str(id)+')')
             str_disliked_post=" ".join(list_of_disliked_posts)
             db.execute(
                 'UPDATE user SET disliked_posts=?'
                 ' WHERE id = ?',
                 (str_disliked_post,user)
                 )
         db.commit()
         
         


def get_like_dislike_post():
    db = get_db()
    user_info=g.user['id']
    user_new = db.execute(
         'SELECT liked_posts,disliked_posts'
         ' FROM user u'
         ' WHERE id = ?',
         (user_info,)
    ).fetchone()
    return user_new
    
def get_comments(post_id):
    db = get_db()
    comments = db.execute(
        'SELECT id,body,created,publisher_id,post_id'
        ' FROM comment'
        ' WHERE post_id = ? ',
        (post_id,)
    ).fetchall()
    return comments
    
    
def get_comment(id):
    db = get_db()
    comment = db.execute(
        'SELECT id,body,created,publisher_id,post_id'
        ' FROM comment'
        ' WHERE id = ? ',
        (id,)
    ).fetchone()
    return comment    

#shift-tab
def add_comment(post_id, publisher_id, body):
      db = get_db()
      db.execute(
         'INSERT INTO comment (post_id, publisher_id, body)'
         ' VALUES (?, ?, ?)',
         (post_id, publisher_id, body)
         )
      db.commit()


def get_name_publisher(publisher_id):
    db = get_db()
    publisher = db.execute(
        'SELECT username'
        ' FROM user u JOIN comment c ON u.id = c.publisher_id'
        ' WHERE u.id = ?',
        (publisher_id,)
    ).fetchone()
    return publisher

def get_all_posts():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username,tag,thumbnail'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return posts
    

def display_per_page(posts,page,per_page):
    i=0
    posts_per_page=[]
    for post in posts:
        #print(post.keys())
        if i//per_page==(page-1):
            posts_per_page.append(post)
        i+=1
    return posts_per_page
#change to local zone timestamp
#https://stackoverflow.com/questions/14814433/how-to-change-timestamp-of-sqlite-db-to-local-timestamp 




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
        #print('ball')
        # check if the post request has the file part
        thumbnail=None
        if 'file' not in request.files:
            flash('file not in request.files')
            #print('hdfhdh')
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path_picture=os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            thumbnail=filename
            file.save(path_picture)
        elif not(allowed_file(file.filename)):
            flash('not allowed file')
            
        return thumbnail



# ...

#TEST!!!
@bp.route('/rss')
def rss():
    fg = FeedGenerator()
    fg.title('hello')
    fg.description('hello to my fellows')
    fg.link(href='http://127.0.0.1:5000')

    for article in get_last_posts(): # get_last_posts() returns a list of articles from somewhere
        fe = fg.add_entry()
        fe.title(article['title'])
        fe.link(href=article['url'])
        fe.description(article['content'])
        #fe.guid(article.id, permalink=False) # Or: fe.guid(article.url, permalink=True)
        fe.author(name=article['author'])
        fe.pubDate(article['created_at'])

    response = make_response(fg.rss_str())
    response.headers.set('Content-Type', 'application/rss+xml')
    return response
    
def get_last_posts():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username,tag,thumbnail'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
        ' LIMIT 3'
    )
    all_rss=[]
    for post in posts:
        print(post['title'])
        fg=rss_post(post)
        all_rss.append(fg)
    return all_rss
    

def rss_post(post):
    fg={}
    fg['title']=post['title']
    fg['url']='http://127.0.0.1:5000/post/'+str(post['id'])
    fg['content']=post['body']
    #fg.guid(post['id'], permalink=False) # Or: fe.guid(article.url, permalink=True)
    fg['author']=post['username']
    #print(pytz.utc.localize(post['created']))
    fg['created_at']=pytz.utc.localize(post['created'])
    #print(fg)
    return fg
    

