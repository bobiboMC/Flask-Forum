from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

#import json
from datetime import datetime
from datetime import timedelta
from flaskr import time_zones #later for add country register



bp = Blueprint('blog', __name__)

#@bp.route('/',defaults={'page': '1'}) # for normal state:@bp.route('/')
@bp.route('/<int:page>',defaults={'page': '1'})
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
                            amount_posts=amount_posts,tag_selected=args.get("tag"),name_selected=args.get("filter_page"))

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    tags=['football','rap','movies']
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tag = request.form['tag']
        error = None

        if not title:
            error = 'Title is required.'
        
        elif tag not in tags:
            error = 'illegal tag.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, tag)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], tag)
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
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tag = request.form['tag']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?,tag = ?'
                ' WHERE id = ?',
                (title, body, tag, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))



#@bp.route('/filter', methods=['GET'])
#@login_required
#def filter_posts():
    #args = request.args 
    #print(args.get("filter_page"),'filter_page')#for get request
    #filter_by=args.get("filter_page")
    #posts=get_all_posts()
    #filtered_posts=[]
    #for post in posts:
        #print(post['title'].startswith(filter_by),post['title'])
        #if post['title'].startswith(filter_by):
            #filtered_posts.append(post['title'])
            #print('yes')
    
    #print(filtered_posts)
    #return redirect(url_for('blog.index',filtered_posts=filtered_posts))
    
    
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



#@bp.route('/tag/<name_tag>', methods=('GET', 'POST'))
#@login_required
#def tag_post(name_tag,posts):
   #filter_posts_by_tag=[]
   #for post in posts:
        #if name_tag==post['tag']:
            #filter_posts_by_tag.append(post['id'])

    #return redirect(url_for('blog.index'),posts=filter_posts_by_tag)


    
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

    return render_template(
                            'blog/show.html',post=my_post,user=user_new,
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
        'SELECT p.id, title, body, created, author_id, username,tag'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return posts

def display_per_page(posts,page,per_page):
    i=0
    posts_per_page=[]
    for post in posts:
        if i//per_page==(page-1):
            posts_per_page.append(post)
        i+=1
    return posts_per_page
#change to local zone timestamp
#https://stackoverflow.com/questions/14814433/how-to-change-timestamp-of-sqlite-db-to-local-timestamp 


