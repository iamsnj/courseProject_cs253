#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 08:43:07 2020

@author: sanjay
"""


from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms import validators

class Sign_In(Form):
    userId = StringField('UserId', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Submit')