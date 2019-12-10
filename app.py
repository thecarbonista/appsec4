from flask import render_template, url_for, flash, redirect, request, Markup, session
from . import app, db, bcrypt
from .forms import RegistrationForm, LoginForm, PostForm, AdminQuery, HistoryForm
from .models import User, LoginHistory, Post
from flask_login import login_user, current_user, logout_user, login_required
import subprocess
from datetime import datetime



@app.route("/spell_check", methods=['GET', 'POST'])
@login_required
def spell_check():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(content=form.content.data, author=current_user)

        text_file = open(r"usertext.txt", "w+")
        text_file.write(form.content.data)
        text_file.close()

        f = open("results.txt", "w+")
        subprocess.call(["./a.out", "./usertext.txt", "./wordlist.txt"], stdout=f)

        with open("results.txt") as f:
            read_data = f.read()
        f.close()
        post.results = read_data
        db.session.add(post)
        db.session.commit()

        success_message = 'Success'
        return render_template('result.html', content=form.content.data, results=post.results)
    else:
        success_message = 'Failure'

    return render_template('spell_check.html', title='Spell Check', form=form, success=success_message)



@app.route("/register", methods=['GET', 'POST'])
def register():
    success_message = ''
    if current_user.is_authenticated:
        success_message = 'Success'
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            twofactor = form.twofactor.data
            user = User(username=form.username.data, password=hashed_password, twofactor=twofactor)
            db.session.add(user)
            db.session.commit()
            success_message = 'Success'
        else:
            success_message = 'Failure'

    return render_template('register.html', title='Register', form=form,  success=success_message)


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    success_message = 'Failure'
    if current_user.is_authenticated:
        success_message = 'Success'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data) and (user.twofactor == form.twofactor.data):
            login_user(user)

            login_history = LoginHistory(username=form.username.data, user_id=user.id, login_time=datetime.now(), logout_time='N/A')
            db.session.add(login_history)
            db.session.commit()
            session['user_id'] = user.id
            session['id'] = login_history.id
            session['username'] = login_history.username
            success_message = 'Success'
        else:
            success_message = 'Failure'
    if request.method == 'GET':
        success_message = ''
    return render_template('login.html', title='Login', form=form, result=success_message)

@app.route("/history", methods=['GET', 'POST'])
@login_required
def history():
    if current_user.get_is_admin():
        users = User.query.all()
        form = AdminQuery()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            username = user.username
            user_id = user.id
            numqueries = Post.query.filter_by(user_id=user_id).count()
            posts = Post.query.filter_by(user_id=user_id)
            return render_template('history.html', posts=posts, userquery=username, user_id=user_id, numqueries=numqueries)
        return render_template('admin.html', form=form, users=users)
    else:
        numqueries = Post.query.filter_by(user_id=session['user_id']).count()
        posts = Post.query.filter_by(user_id=session['user_id'])
        username = session['username']
        user_id = session['user_id']
        return render_template('history.html', posts=posts, numqueries=numqueries, user_id=user_id, userquery=username)

@app.route("/history/query<int:queryid>", methods=['GET'])
@login_required
def post(queryid):
    user = Post.query.filter_by(id=queryid).first()
    if user.user_id == session['user_id']:
        posts = Post.query.filter_by(id=queryid)
        return render_template('query.html', posts=posts)
    elif current_user.get_is_admin():
        posts = Post.query.filter_by(id=queryid)
        return render_template('query.html', posts=posts)
    else:
        return render_template('noauth.html')

@app.route('/login_history', methods=['GET', 'POST'])
@login_required
def login_history():
    if current_user.get_is_admin():
        histories = LoginHistory.query.all()
        form = HistoryForm()
        if form.validate_on_submit():
            user = LoginHistory.query.filter_by(user_id=form.user_id.data).first()
            user_id = user.user_id
            history = LoginHistory.query.filter_by(user_id=form.user_id.data)
            return render_template('admin_view.html', histories=histories, history=history, user_id=user_id)
        return render_template('login_history.html', form=form, histories=histories)
    else:
        return render_template('noauth.html')

@app.route("/logout")
def logout():
    log = LoginHistory.query.filter_by(id=session['id']).first()
    log.logout_time = datetime.now()
    db.session.commit()
    session.pop('username', None)
    session.pop('id', None)
    logout_user()

    return redirect(url_for('login'))



