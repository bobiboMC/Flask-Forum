import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash


import secrets
import string
from oauth2 import send_email_1_1


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'email is required.'
        
        m_gmail = email.endswith('@gmail.com')
        m_outlook = email.endswith('@outlook.com')
        if not(m_gmail or m_outlook):
            error = 'format email is wrong.'
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, email) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password),email),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
    
    
    
@bp.route('/forget_password', methods=('POST','GET'))
def forget_pwd_outlook():
    if request.method == 'POST':
        if request.form.get('reset_email'):
                #print(request.form.get('reset_email'))
                reset_pwd=OTP()
                session['reset'] = reset_pwd
                session['email'] = request.form.get('reset_email')
                ##TEST
                print(emails_company())
                ##TEST
                email_sender=emails_company()['email']
                send_email_1_1.send_exp_outlook_email(reset_pwd,email_sender,
                                                        session['email'])
                #send_email_1.send_exp_gmail_email(reset_pwd)
                #send_email_2.send_email_gmail()
                return render_template('auth/send_reset_pwd.html',enter_email=True)   
        reset_password=session.get('reset')
        entered_password = request.form['password_reset']
        print(entered_password,reset_password)
        if reset_password==entered_password:
            print('kawai magic')
            email=session['email']
            return redirect(url_for('auth.create_new_pwd',email=email))
        else:
            flash('kawai magic')
    #enter_email=request.form.get('enter_email')
    #print(enter_email)

    return render_template('auth/send_reset_pwd.html',enter_email=False)    
    

def OTP():
    secretsGenerator = secrets.SystemRandom()
    digits = string.digits #0123456789
    reset_pwd=''
    for i in range(0,6):
        secure_choice = secretsGenerator.choice(digits)
        reset_pwd+=secure_choice
    print(reset_pwd)
    return reset_pwd

def upadte_password(email,password):
       db = get_db() 
       db.execute(
             'UPDATE user SET password=?'
             ' WHERE email = ?',
             (generate_password_hash(password),email)
             )
       db.commit() 

@bp.route('/create_new_password', methods=('POST','GET'))
def create_new_pwd():
       if request.method == 'POST':
            email=session['email']
            password=request.form['new_pwd']
            comfirm_password=request.form['confirm_new_pwd']
            if password!=comfirm_password: #different password from confirm
                flash('confirm is wrong')
                return render_template('auth/create_new_pwd.html') 
            upadte_password(email,password)
            session.clear()
            return redirect(url_for('auth.login'))    
            
       return render_template('auth/create_new_pwd.html')    

