__author__ = 'BroZapp'
from wtforms import Form, BooleanField, StringField, PasswordField, SelectMultipleField,\
    validators, FileField, TextAreaField


class RegistrationForm(Form):
    username = StringField('Username', [validators.length(min=4, max=25)])
    real_name = StringField('Author Name', [validators.length(min=1, max=25)])
    email = StringField('Email Address', [validators.email()])
    password = PasswordField('New Password', [validators.DataRequired(),
                                              validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class LogInForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')


class BlogForm(Form):
    title = StringField('Title', [validators.length(min=1)])
    headIMG = FileField('Upload Headline Image')
    bodyHTML = FileField('Upload Body')
    textHTML = TextAreaField('HTML', [validators.length(min=1)], id='textinput')
    tags = StringField('Tags')
    projects = SelectMultipleField('Attached projects')
    delete = BooleanField('Delete')


class CommentForm(Form):
    # make it so you have to write at least a 5 letter word.
    # No just 'fuck' on my comments thread, but 'fuck.' is totally fine.
    # punctuate that bitch!
    comment_text = TextAreaField('Write your comment here!', [validators.length(min=5)])


class ProjectForm(Form):
    title = StringField('Title', [validators.length(min=1)])
    headIMG = FileField('Upload Headline Image')
    abstract = TextAreaField('Abstract', [validators.length(min=1)], id='textinput')
    tags = StringField('Tags')

class CheckoutForm(Form):
    first_name = StringField('First name', [validators.length(min=1)])
    last_name = StringField('Last name', [validators.length(min=1)])
    address_1 = StringField('Address 1', [validators.length(min=1)])
    address_2 = StringField('Address 2', [validators.length(min=1)])
    city = StringField('City/Town', [validators.length(min=1)])
    state = StringField('State', [validators.length(min=1)])
    zip_code = StringField('Zip Code', [validators.length(min=1)])