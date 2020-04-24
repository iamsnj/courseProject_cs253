#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 22:22:08 2020

@author: sanjay
"""


from wtforms import Form, StringField, PasswordField, SubmitField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class Register(Form):
    username = StringField('Username', [validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])                                               
    submit = SubmitField('Sign Up')

class Sign_In(Form):
    whichUser = RadioField('Login As', choices = [('A','Admin'),('T','TA')], default='A')  
    userId = StringField('UserId', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Submit')

class change_password(Form):
    password = PasswordField('New Password', [validators.DataRequired()])
    confirm = PasswordField('Confirm Your Password', [validators.DataRequired()])
    submit = SubmitField('Submit')