from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.auth.forms import LoginForm, NewProjectForm
from app.auth.forms import RegistrationForm
from app.const.constants import PUBLIC
from app.const.methods import append_id_to_file
from app.models import User, Project


@app.route('/')
@app.route('/home')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Home Page')


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
            userid=form.userid.data,
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
            locationid=form.locationid,
            privacy=False if form.privacy.data == PUBLIC else True,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        append_id_to_file(form.userid.data[4:])
        append_id_to_file(form.locationid[4:])
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    print('Registration Form Error section 3:', form.errors)
    return render_template('auth/register.html', title='Register', form=form)


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)


@app.route('/edit_profile/<username>', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('edit_profile.html', user=user)


@app.route('/my_projects/<username>')
@login_required
def my_projects(username):
    user = User.query.filter_by(username=username).first_or_404()
    projects = Project.query.filter_by(userid=user.userid).all()
    return render_template('user/my_projects.html', user=user, projects=projects)


@app.route('/create_project/<username>', methods=['GET', 'POST'])
@login_required
def create_project(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = NewProjectForm()
    print('Project Form Error section 1:', form.errors)
    if form.validate_on_submit():
        print('Project Form Error section 2:', form.errors)
        project = Project(
            projectid=form.projectid.data,
            userid=current_user.userid,
            name=form.name.data,
            fields=form.fields.data
        )
        project.set(
            members_required=form.members_required.data,
            members=form.members.data,
            member_list=form.member_list.data,
            project_description=form.project_description.data,
            channel=form.channel.data
        )
        db.session.add(project)
        db.session.commit()
        append_id_to_file(form.projectid.data[4:])
        flash('Congratulations, your New Project has been created!')
        return redirect(url_for('my_projects', username=username))
    return render_template('user/new_project.html', user=user, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
