__author__ = 'BroZapp'
from wtforms import Form, BooleanField, StringField, PasswordField, validators, FileField, TextAreaField


class RegistrationForm(Form):
    username = StringField('Username', [validators.length(min=4, max=25)])
    realname = StringField('Author Name', [validators.length(min=1, max=25)])
    email = StringField('Email Address', [validators.length(min=6, max=35)])
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
    textHTML = TextAreaField('HTML', [validators.length(min=1)])

class CommentForm(Form):
    # make it so you have to write at least a 5 lietter word.
    # No just 'fuck' on my comments thread, but 'fuck.' is totally fine.
    # punctuate that bitch!
    comment_text = TextAreaField('Write your comment here!', [validators.length(min=5)])