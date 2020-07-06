from flask import render_template, url_for, flash, redirect, request, Response, Flask
from App import app, db, bcrypt, emotion_check
from App.forms import RegistrationForm, LoginForm, PostForm,PatientForm
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


@app.route("/register", methods=['GET', 'POST'])
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


@app.route("/manage/patient", methods=['GET', 'POST'])
@login_required
def patient_manage():
    notice = Notice_Post.query.all()
    patient = Patient.query.all()
    form = PatientForm()
    if form.validate_on_submit():
        post = Patient(name=form.name.data, sex=form.sex.data, age=form.age.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('patient_manage'))
    return render_template('manage_patient.html', notice=notice, patient=patient, form=form, title='Patient Management', legend='Register Patient')


@app.route("/manage/patient_delete", methods=['GET', 'POST'])
@login_required
def patient_delete():
    id = request.args.get('id')
    patient = Patient.query.filter_by(id=id).first()
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('patient_manage'))
    return render_template('manage_patient.html', title='Delete Patient List')


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


@app.route("/manage/staff", methods=['GET', 'POST'])
def worker_manage():
    worker = Worker.query.all()
    return render_template('manage_worker.html', worker=worker)


@app.route("/manage/worker_delete", methods=['GET', 'POST'])
def worker_delete():
    id = request.args.get('id')
    worker = Worker.query.filter_by(id=id).first()
    db.session.delete(worker)
    db.session.commit()
    return redirect(url_for('worker_manage'))


@app.route("/emotioncheck")
def emotioncheck():
    notice = Notice_Post.query.all()
    return render_template('emotioncheck.html', notice=notice, title='Emotion Check')


@app.route('/emotioncheck/video_feed')
def video_feed():
    return Response(emotion_check.gen(emotion_check.VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')