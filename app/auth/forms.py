from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember_me = BooleanField('Ghi nhớ đăng nhập')
    submit = SubmitField('Đăng nhập')

class RegistrationForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[
        DataRequired(),
        Length(min=3, max=64, message='Tên đăng nhập phải có từ 3 đến 64 ký tự')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Email không hợp lệ'),
        Length(max=120, message='Email không được vượt quá 120 ký tự')
    ])
    
    password = PasswordField('Mật khẩu', validators=[
        DataRequired(),
        Length(min=8, message='Mật khẩu phải có ít nhất 8 ký tự')
    ])
    
    password2 = PasswordField(
        'Xác nhận mật khẩu',
        validators=[
            DataRequired(),
            EqualTo('password', message='Mật khẩu không khớp')
        ]
    )
    
    submit = SubmitField('Đăng ký')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Tên đăng nhập đã được sử dụng. Vui lòng chọn tên khác.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email đã được sử dụng. Vui lòng dùng email khác.')