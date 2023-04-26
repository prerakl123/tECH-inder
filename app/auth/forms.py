import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, RadioField, TextAreaField, SubmitField, \
    IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, Length

from app import app
from app.const.constants import M, F, PN, OT, PUBLIC, PRIVATE
from app.models import User

app.app_context().push()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    userid = ''
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Full Name', validators=[DataRequired()])
    dob = DateField('Date of Birth')
    gender = SelectField('Gender', choices=[('M', M), ('F', F), ('PN', PN), ('OT', OT)])
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
    locationid = ''
    privacy = BooleanField('Make Profile Private')
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
    projectid = ''
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
    channel = ''
    timestamp = datetime.datetime.now()
    submit = SubmitField('Create')

    # def validate_name(self, name):
    #     project = Project.query.filter_by(name=name).first()
    #     if project is not None:
    #         raise ValidationError(
    #             'Please use a different name for the project. '
    #             'Try using numbers, etc to create a unique project name.'
    #         )


class EditProfileForm(FlaskForm):
    userid = ''
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Full Name', validators=[DataRequired()])
    dob = DateField('Date of Birth')
    gender = SelectField('Gender', choices=[('M', M), ('F', F), ('PN', PN), ('OT', OT)])
    interests = TextAreaField(
        "Topics I'm interested in",
        description='Insert the topics you\'re interested in or proficient in separated by a semicolon (;).'
    )
    github_profile = StringField('GitHub profile link (or username)')
    about_me = TextAreaField(
        'About me',
        description='Write a short description about yourself. Can include your achievements, things you are interested'
                    ' in, your goals, etc',
        validators=[Length(min=0, max=500)]
    )
    locationid = ''
    privacy = BooleanField('Make Profile Private')
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = ''
    timestamp = datetime.datetime.now()
    submit = SubmitField('Update')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
