from flask import render_template, url_for, flash, redirect, request
from App import app, db, bcrypt
from App.forms import RegistrationForm, LoginForm
from App.models import Worker, Patient, Care_Post, Notice_Post
from flask_login import login_user, current_user, logout_user


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
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
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/register", methods=['GET','POST'])
def register():
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
    return render_template('register.html', title='Register', form=form)


@app.route("/emotioncheck")
def emotioncheck():
    return render_template('emotioncheck.html', title='Emotion Check')

@app.route("/admin")
def admin():
    return render_template('admin.html', title='Administrator Only')