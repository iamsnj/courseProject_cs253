#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 16:31:39 2020

@author: sanjay
"""

from login import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(40))
    password = db.Column(db.String)
    
class ta_email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40))

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(40))
    password = db.Column(db.String)
    
class mt_students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    father = db.Column(db.String(40))
    email = db.Column(db.String(40))
    phone = db.Column(db.String(20))
    dob = db.Column(db.String(10))
    score = db.Column(db.Integer)
    gate = db.Column(db.Integer)
    disc = db.Column(db.String)
    comments = db.Column(db.String, nullable=True)
    
class phd_students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    father = db.Column(db.String(40))
    email = db.Column(db.String(40))
    phone = db.Column(db.String(20))
    dob = db.Column(db.String(10))
    score = db.Column(db.Integer)
    gate = db.Column(db.Integer)
    disc = db.Column(db.String)
    comments = db.Column(db.String, nullable=True)
