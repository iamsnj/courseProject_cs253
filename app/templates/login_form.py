#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 22:22:08 2020

@author: sanjay
"""


from wtforms import Form, StringField, PasswordField, SubmitField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class Register(Form):
    username = StringField('Username', [validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
    # number = IntegerField('Number')
    submit = SubmitField('Sign Up')