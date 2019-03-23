from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,ValidationError
from ajaira.models import User,Post
from flask_login import current_user
from flask_wtf.file import FileField,FileAllowed

class RegistrationForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(min=2)])
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])

    submit=SubmitField("Register")


    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Sorry this email is Taken please Try another!")


class LoginForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    remember=BooleanField("remember me")
    submit=SubmitField("Login")

class UpdateForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(min=2)])
    email=StringField("Email",validators=[DataRequired(),Email()])
    picture=FileField("Change profile",validators=[FileAllowed(["jpg","png"])])


    submit=SubmitField("Update")


    def validate_email(self,email):
        if email.data !=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Sorry this email is Taken please Try another!")

class PostForm(FlaskForm):
    title=TextAreaField("Title")
    content=TextAreaField("Content" )
    image=FileField("Image",validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField("Post")
