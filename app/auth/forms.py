import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, RadioField, TextAreaField, SubmitField, \
    IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, Length

from app import app
from app.const.constants import UID, LID, M, F, PN, OT, PUBLIC, PRIVATE, PID, CID
from app.const.methods import generate_id
from app.models import User, Project

app.app_context().push()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    userid = StringField("User ID", default=generate_id(UID))
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Full Name', validators=[DataRequired()])
    dob = DateField('Date of Birth')
    gender = RadioField('Gender', choices=[M, F, PN, OT])
    interests = TextAreaField(
        "Topics I'm interested in",
        description='Insert the topics you\'re interested in or proficient in separated by a semicolon (;).'
    )
    github_profile = StringField('GitHub profile link (or username)')
    about_me = TextAreaField(
        'About me',
        description='Write a short description about yourself. Can include your achievements, things you are interested'
                    ' in, your goals, etc'
    )
    locationid = generate_id(LID)
    privacy = RadioField('Select Privacy', choices=[PUBLIC, PRIVATE])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    timestamp = datetime.datetime.now()
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_userid(self, userid):
        user = User.query.filter_by(userid=userid.data).first()
        if user is not None:
            raise ValidationError('Please refresh the form for a new UID.')


class NewProjectForm(FlaskForm):
    projectid = StringField("Project ID", default=generate_id(PID))
    userid = ''
    name = StringField(
        'Project Name', default='New Project', validators=[DataRequired()])
    fields = TextAreaField(
        'Fields',
        description='All the fields this project covers (ex-CS, Mechanical, Electronics, etc)',
        validators=[DataRequired()]
    )
    members_required = IntegerField('Members Required', validators=[DataRequired()])
    members = IntegerField('Current No. of Members', default='0')
    member_list = TextAreaField('Members', default='Can\'t be filled right now!')
    project_description = TextAreaField('Project Description', validators=[Length(max=100), DataRequired()])
    owner = True
    channel = StringField('Channel', default=generate_id(CID))
    timestamp = datetime.datetime.now()
    submit = SubmitField('Create')

    # def validate_name(self, name):
    #     project = Project.query.filter_by(name=name).first()
    #     if project is not None:
    #         raise ValidationError(
    #             'Please use a different name for the project. '
    #             'Try using numbers, etc to create a unique project name.'
    #         )
