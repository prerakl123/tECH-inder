from datetime import datetime, date
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login, app


@login.user_loader
def load_user(id):
    return User.query.get(id)


class User(UserMixin, db.Model):
    userid = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(16))
    interests = db.Column(db.String)
    github_profile = db.Column(db.String(108))
    about_me = db.Column(db.Text)
    locationid = db.Column(db.String(64), db.ForeignKey('location.locationid'))
    privacy = db.Column(db.Boolean)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    projects = db.relationship('Project', backref='author', lazy='dynamic')
    reports = db.relationship('Misconduct', backref='author', lazy='dynamic')
    projects_applied = db.relationship('Applied', backref='member', lazy='dynamic')

    def __init__(self, userid, username, email):
        self.userid = userid
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            md5(self.email.lower().encode('utf-8')).hexdigest(),
            size
        )

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.userid)

    def set(self,
            name: str = None,
            dob: date = None,
            gender: str = None,
            interests: str = None,
            github_profile: str = None,
            about_me: str = None,
            locationid: str = None,
            privacy: bool = None,
            password: str = None,
            last_seen: datetime = None
            ):

        if name:
            self.name = name

        if name:
            self.name = name

        if dob:
            self.dob = dob

        if gender:
            self.gender = gender

        if interests:
            self.interests = interests

        if github_profile:
            self.github_profile = github_profile

        if about_me:
            self.about_me = about_me

        if locationid:
            self.locationid = locationid

        if privacy:
            self.privacy = privacy

        if password:
            self.password_hash = generate_password_hash(password)

        if last_seen:
            self.last_seen = last_seen

    def set_name(self, name):
        self.name = name

    def set_dob(self, dob):
        self.dob = dob

    def set_gender(self, gender):
        self.gender = gender

    def set_interests(self, interests):
        self.interests = interests

    def set_github_profile(self, github_profile):
        self.github_profile = github_profile

    def set_about_me(self, about_me):
        self.about_me = about_me

    def set_location_id(self, locationid):
        self.locationid = locationid

    def set_privacy(self, privacy):
        self.privacy = privacy

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_last_seen(self, last_seen):
        self.last_seen = last_seen


class Project(db.Model):
    projectid = db.Column(db.String(64), primary_key=True)
    userid = db.Column(db.String(64), db.ForeignKey('user.userid'))
    name = db.Column(db.String(64))
    fields = db.Column(db.String(512))
    members_required = db.Column(db.Integer)
    members = db.Column(db.Integer)
    member_list = db.Column(db.String(512))
    project_description = db.Column(db.String(512))
    owner = db.Column(db.Boolean, default=True)
    channel = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, projectid, userid, name, fields):
        self.projectid = projectid
        self.userid = userid
        self.name = name
        self.fields = fields

    def __repr__(self):
        return '<Project {}>'.format(self.projectid)

    def get_id(self):
        return str(self.projectid)

    def set(self,
            name: str = None,
            fields: str = None,
            members_required: int = None,
            members: int = None,
            member_list: str = None,
            project_description: str = None,
            channel: str = None,
            ):
        if name:
            self.name = name

        if fields:
            self.fields = fields

        if members_required:
            self.members_required = members_required

        if members:
            self.members = members

        if member_list:
            self.member_list = member_list

        if project_description:
            self.project_description = project_description

        if channel:
            self.channel = channel

    def set_name(self, name):
        self.name = name

    def set_fields(self, fields):
        self.fields = fields

    def set_members_required(self, members_required):
        self.members_required = members_required

    def set_members(self, members):
        self.members = members

    def set_member_list(self, member_list):
        self.member_list = member_list

    def set_project_description(self, project_description):
        self.project_description = project_description


class Misconduct(db.Model):
    causeid = db.Column(db.String(64), primary_key=True)
    userid = db.Column(db.String(64), db.ForeignKey('user.userid'))
    misconduct_userid = db.Column(db.Integer)
    block = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Misconduct {}>'.format(self.causeid)

    def get_id(self):
        return str(self.causeid)


class Message(db.Model):
    messageid = db.Column(db.String(64), primary_key=True)
    userid = db.Column(db.String(64), db.ForeignKey('user.userid'))
    channel = db.Column(db.String(16))
    content = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.messageid)

    def get_id(self):
        return str(self.messageid)


class Likes(db.Model):
    likeid = db.Column(db.String(64), primary_key=True)
    userid = db.Column(db.String(64), db.ForeignKey('user.userid'))
    is_liked = db.Column(db.Boolean, default=True)
    projectid = db.Column(db.String(64), db.ForeignKey('project.projectid'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Likes {}>'.format(self.projectid)

    def get_id(self):
        return str(self.likeid)


class Applied(db.Model):
    appliedid = db.Column(db.String(64), primary_key=True)
    userid = db.Column(db.String(64), db.ForeignKey('user.userid'))
    projectid = db.Column(db.String(64), db.ForeignKey('project.projectid'))
    body = db.Column(db.String(512))
    accepted = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Applied {}>'.format(self.body)

    def get_id(self):
        return str(self.appliedid)


class Location(db.Model):
    locationid = db.Column(db.Integer, primary_key=True)
    lat_long = db.Column(db.String(64))
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Location {}>'.format(self.body)

    def get_id(self):
        return str(self.locationid)


@app.before_first_request
def create_tables():
    db.create_all()
