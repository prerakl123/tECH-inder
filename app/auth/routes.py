from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.auth.forms import LoginForm, NewProjectForm, EditProfileForm, RegistrationForm, ResetPasswordRequestForm, \
    EmptyForm, ResetPasswordForm
from app.const.constants import PUBLIC, PID, UID, GID, CID
from app.const.methods import generate_id
from app.email import send_password_reset_email
from app.models import User, Project


@app.route('/')
@app.route('/home')
@app.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    projects = current_user.followed_projects().paginate(
        page=page,
        per_page=app.config['PROJECTS_PER_PAGE'],
        error_out=False
    )
    next_url = url_for('index', page=projects.next_num) if projects.has_next else None
    prev_url = url_for('index', page=projects.prev_num) if projects.has_prev else None
    return render_template("index.html", title='Home Page', projects=projects.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    print('Registration Form Error section 1: ', form.errors)
    if form.validate_on_submit():
        print('Registration Form Error section 2:', form.errors)
        user = User(
            userid=generate_id(UID, append=True),
            username=form.username.data,
            email=form.email.data
        )
        user.set(
            name=form.name.data,
            dob=form.dob.data,
            gender=form.gender.data,
            interests=form.interests.data,
            github_profile=form.github_profile.data,
            about_me=form.about_me.data,
            locationid=generate_id(GID, append=True),
            privacy=0 if form.privacy.data == PUBLIC else True,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    print('Registration Form Error section 3:', form.errors)
    return render_template('auth/register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['POST', 'GET'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password', methods=['POST', 'GET'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('auth/reset_password.html', form=form)


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('profile.html', user=user, form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username       = form.username.data
        current_user.name           = form.name.data
        current_user.dob            = form.dob.data
        current_user.gender         = form.gender.data
        current_user.interests      = form.interests.data
        current_user.github_profile = form.github_profile.data
        current_user.about_me       = form.about_me.data
        current_user.privacy        = form.privacy.data
        current_user.email          = form.email.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data       = current_user.username
        form.name.data           = current_user.name
        form.dob.data            = current_user.dob
        form.gender.data         = current_user.gender
        form.interests.data      = current_user.interests
        form.github_profile.data = current_user.github_profile
        form.about_me.data       = current_user.about_me
        form.privacy.data        = current_user.privacy
        form.email.data          = current_user.email
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/my_projects/<username>')
@login_required
def my_projects(username):
    user = User.query.filter_by(username=username).first_or_404()
    projects = Project.query.filter_by(userid=user.userid).all()
    form = EmptyForm()
    return render_template('user/my_projects.html', user=user, projects=projects, form=form)


@app.route('/create_project/<username>', methods=['GET', 'POST'])
@login_required
def create_project(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = NewProjectForm()
    print('Project Form Error section 1:', form.errors)
    if form.validate_on_submit():
        print('Project Form Error section 2:', form.errors)
        project = Project(
            projectid=generate_id(PID, append=True),
            userid=current_user.userid,
            name=form.name.data,
            fields=form.fields.data
        )
        project.set(
            members_required=form.members_required.data,
            members=0,
            member_list=form.member_list.data,
            project_description=form.project_description.data,
            channel=generate_id(CID, append=True)
        )
        db.session.add(project)
        db.session.commit()
        flash(f'Your New Project: {project.name} is live!')
        return redirect(url_for('my_projects', username=username))
    return render_template('user/new_project.html', user=user, form=form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('profile', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('profile', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('profile', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(
        Project.timestamp.desc()
    ).paginate(
        page=page,
        per_page=app.config['PROJECTS_PER_PAGE'],
        error_out=False
    )
    next_url = url_for('explore', page=projects.next_num) if projects.has_next else None
    prev_url = url_for('explore', page=projects.prev_num) if projects.has_prev else None
    return render_template('index.html', title='Explore', projects=projects.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
