from flask import render_template, url_for, flash, redirect, request
from App import app, db, bcrypt
from App.forms import RegistrationForm, LoginForm, PostForm
from App.models import Worker, Patient, Care_Post, Notice_Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    posts = Care_Post.query.all()
    notice = Notice_Post.query.all()
    return render_template('home.html', posts=posts, notice=notice)


@app.route("/login", methods=['GET', 'POST'])
def login():
    notice = Notice_Post.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if form.validate_on_submit():
        user = Worker.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if form.email.data == 'admin@gmail.com' and form.password.data == 'admin':
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('admin'))
            else:
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Pleach check again', 'danger')
    return render_template('login.html', title='Login', form=form, notice=notice)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/register", methods=['GET','POST'])
def register():
    notice = Notice_Post.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        worker = Worker(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(worker)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, notice=notice)


@app.route("/post/report", methods=['GET', 'POST'])
@login_required
def new_post():
    notice = Notice_Post.query.all()
    form = PostForm()
    if form.validate_on_submit():
        post = Care_Post(title=form.title.data, content=form.content.data, worker=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, notice=notice, legend='New Post')


@app.route("/emotioncheck")
def emotioncheck():
    notice = Notice_Post.query.all()
    return render_template('emotioncheck.html', notice=notice, title='Emotion Check')


@app.route("/manage/patient")
def patient_manage():
    notice = Notice_Post.query.all()
    return render_template('manage_patient.html', notice=notice, title='Patient Management')


@app.route("/admin")
def admin():
    notice = Notice_Post.query.all()
    return render_template('admin.html', title='Administrator Only', notice=notice)

@app.route("/post/notice", methods=['GET', 'POST'])
def notice_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Notice_Post(title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('admin'))
    return render_template('notice_post.html', form=form, legend='Notice Post')

@app.route("/manage/staff")
def worker_manage():
    notice = Notice_Post.query.all()
    return render_template('manage_worker.html', notice=notice)