# forms.py HvS Assets
from flask_wtf import Form
from wtforms import TextField, DateField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class AddAsset(Form):
    asset_id=IntegerField('Priority')
    asset_type=TextField('asset_type', validators=[DataRequired()])
    asset_descr=TextField('asset_descr', validators=[DataRequired()])
#    install_date=DateField('install_date (mm/dd/yyyy)', validators=[DataRequired()])
    install_date=DateField('install_date (dd/mm/yyyy)', validators=[DataRequired()], format='%d/%m/%Y')
    priority=SelectField('priority',validators=[DataRequired()], choices=[('1','1'),('2','2'),('3','3')])
    status=IntegerField('status')
    posted_date=DateField('Posted Date dd/mm/yyyy', validators=[DataRequired()], format='%d/%m/%Y')

class RegisterForm(Form):
#    name=TextField('Username', validators=[DataRequired(), Length(min=6, max=25)])
#    email=TextField('Email', validators=[DataRequired(), Length(min=6, max=40)])
#    password=PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
#    confirm=PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    name=TextField('Username')
    email=TextField('Email')
    password=PasswordField('Password', validators=[DataRequired(), Length(min=5, max=40)])
    confirm=PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])




class LoginForm(Form):
    name=TextField('Username', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    