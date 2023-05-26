from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User
from flask_pagedown.fields import PageDownField
from flask_wtf.recaptcha import RecaptchaField
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

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


class PostForm(FlaskForm):
    post = PageDownField('Say something[This text field can use Markdown.]', validators=[DataRequired()])
    tags = SelectMultipleField(
        'Tag Name',
        validators=[DataRequired()],
        choices=[
            ('Migraine', 'Migraine'),
            ('Allergy', 'Allergy'),
            ('Weight loss', 'Weight loss'),
            ('Menopausal Disorders','Menopausal Disorders'),
            ('Fungal infections', 'Fungal infections'),
            ('Antibiotics','Antibiotics'),
            ('Drugs and Lactation','Drugs and Lactation'),
            ('Cancer','Cancer'),
            ('etc','etc')
        ])
    recaptcha = RecaptchaField('Captcha')
    submit = SubmitField('Submit')