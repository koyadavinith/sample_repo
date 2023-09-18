from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from market.models import user

class Register(FlaskForm):
    def validate_username(self,username_to_check):
        username = user.query.filter_by(username = username_to_check.data).first()
        if username:
            raise ValidationError('Username Already Exists! Try Different username')
        
    def validate_email_id(self,email_to_check):
        email_id = user.query.filter_by(email_id = email_to_check.data).first()
        if email_id:
            raise ValidationError('Email_address Already Exists! Try Different email_address')
        

    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_id = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='New Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class Login(FlaskForm):
    username = StringField(label='User Name:',validators= [DataRequired()])
    password = PasswordField(label = 'Password:',validators = [DataRequired()])
    submit = SubmitField(label = 'Sign in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')