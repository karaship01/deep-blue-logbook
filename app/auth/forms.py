from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
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

class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('E-posta'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Şifre Sıfırlama İste'))

class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Yeni Şifre'), validators=[DataRequired()])
    password_2 = PasswordField(_l('Yeni Şifreyi Tekrar Girin'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Şifre Sıfırla'))