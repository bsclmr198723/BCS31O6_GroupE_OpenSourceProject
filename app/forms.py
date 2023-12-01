from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # def validate_username(self, username):
        # user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different email address.')
        
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RepositoryForm(FlaskForm):
    name = StringField('Repository Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Create Repository')
    
class EditRepositoryForm(FlaskForm):
    name = StringField('Repository Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Update Repository')
    
class IssueForm(FlaskForm):
    title = StringField('Issue title', validators=[DataRequired()])
    description = TextAreaField('Description')
    status = SelectField('Status', coerce=int, validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Issue')