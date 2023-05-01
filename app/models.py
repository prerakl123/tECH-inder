from datetime import datetime, date
from hashlib import md5
from time import time
import jwt

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login, app


@login.user_loader
def load_user(id):
    return User.query.get(id)


followers = db.Table(
    'followers',
    db.Column('follower_id', db.String(64), db.ForeignKey('user.userid')),
    db.Column('followed_id', db.String(64), db.ForeignKey('user.userid'))
)


class User(UserMixin, db.Model):
    userid = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(16))
    interests = db.Column(db.String)
    github_profile = db.Column(db.String(108))
    about_me = db.Column(db.Text)
    locationid = db.Column(db.String(64), db.ForeignKey('location.locationid', use_alter=True))
    privacy = db.Column(db.Boolean)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == userid),
        secondaryjoin=(followers.c.followed_id == userid),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

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

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.userid).count() > 0

    def followed_projects(self):
        followed = Project.query.join(
            followers,
            (followers.c.followed_id == Project.userid)
        ).filter(
                followers.c.follower_id == self.userid
        )
        own = Project.query.filter_by(userid=self.userid)
        return followed.union(own).order_by(Project.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({
            'reset_password': self.userid,
            'exp': time() + expires_in
        },
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            userid = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=['HS256']
            )['reset_password']
        except:
            return
        return User.query.get(userid)

    def get_id(self):
        return str(self.userid)

    def set(self,
            name: str = None,
            username: str = None,
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

        if name is not None:
            self.name = name

        if username is not None:
            self.username = username

        if dob is not None:
            self.dob = dob

        if gender is not None:
            self.gender = gender

        if interests is not None:
            self.interests = interests

        if github_profile is not None:
            self.github_profile = github_profile

        if about_me is not None:
            self.about_me = about_me

        if locationid is not None:
            self.locationid = locationid

        if privacy is not None:
            self.privacy = privacy

        if password is not None:
            self.password_hash = generate_password_hash(password)

        if last_seen is not None:
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
        if name is not None:
            self.name = name

        if fields is not None:
            self.fields = fields

        if members_required is not None:
            self.members_required = members_required

        if members is not None:
            self.members = members

        if member_list is not None:
            self.member_list = member_list

        if project_description is not None:
            self.project_description = project_description

        if channel is not None:
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


# class Likes(db.Model):
#     likeid = db.Column(db.String(64), primary_key=True)
#     userid = db.Column(db.String(64), db.ForeignKey('user.userid'))
#     is_liked = db.Column(db.Boolean, default=True)
#     projectid = db.Column(db.String(64), db.ForeignKey('project.projectid'))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#
#     def __repr__(self):
#         return '<Likes {}>'.format(self.projectid)
#
#     def get_id(self):
#         return str(self.likeid)


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
    userid = db.Column(db.Integer, db.ForeignKey('user.userid', use_alter=True))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Location {}>'.format(self.body)

    def get_id(self):
        return str(self.locationid)


@app.before_first_request
def create_tables():
    db.create_all()
