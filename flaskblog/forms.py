
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
	username = StringField("Username",validators=[DataRequired(),Length(min=4, max=25)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])

	submit = SubmitField('サインイン')

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
		     raise ValidationError('このアカウントは、既に使用されています。他のアカウントをお願いします。') 

	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('このメールアドレスは、既に使用されています。他のメールアドレスをお願いします。')

class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators={DataRequired()})
	remember = BooleanField('Remember Me')
	submit = SubmitField('ログイン')

class UpdateAccountForm(FlaskForm):
	username = StringField('ユーザー名',validators=[DataRequired(),Length(min=2,max=20)])
	email = StringField('メールアドレス',validators=[DataRequired(),Email()])
	picture = FileField('写真を更新する'	,validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('更新')

	def validate_username(self,username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError("他のユーザー名をお願いします。")

	def validata_email(self,email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError("他のメールアドレスをお願いします。")

class PostForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired()])
	content = TextAreaField('content',validators=[DataRequired()])
	submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	submit = SubmitField('パスワードをリセットする')

	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('このアカウントには、メールアドレスがありません。最初にメールアドレスを登録する必要があります。')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])

	submit = SubmitField('Reset Password')
