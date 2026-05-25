from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
import sqlalchemy as sa
from app import db
from app.models import User
from flask_babel import lazy_gettext as _l

class LoginForm(FlaskForm):
    username = StringField(_l('Kullanıcı Adı'), validators=[DataRequired()])
    password = PasswordField(_l('Şifre'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Beni Hatırla'))
    submit = SubmitField(_l('Giriş Yap'))

class RegistrationForm(FlaskForm):
    username = StringField(_l('Kullanıcı Adı'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Şifre'), validators=[DataRequired()])
    password_2 = PasswordField(_l('Şifreyi Onayla'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Kayıt Ol'))

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError(_l('Lütfen farklı bir kullanıcı adı seçin.'))

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError(_l('Lütfen farklı bir email adresi kullanın.'))

class EditProfileForm(FlaskForm):
    username = StringField(_l('Kullanıcı Adı'), validators=[DataRequired()])
    about_me = TextAreaField(_l('Hakkımda'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Kaydet'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(User.username == username.data))
            if user is not None:
                raise ValidationError(_l('Lütfen farklı bir kullanıcı adı seçin.'))

class ProjectForm(FlaskForm):
    title = StringField(_l('Proje Başlığı'), validators=[DataRequired()])
    body = TextAreaField(_l('Proje Detayları'), validators=[DataRequired(), Length(min=1, max=500)])
    technologies = StringField(_l('Kullanılan Teknolojiler'), validators=[DataRequired()])
    submit = SubmitField(_l('Projeyi Ekle'))

class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('E-posta'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Şifre Sıfırlama İste'))

class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Yeni Şifre'), validators=[DataRequired()])
    password_2 = PasswordField(_l('Yeni Şifreyi Tekrar Girin'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Şifre Sıfırla'))