#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 22:20:36 2020

@author: sanjay
"""


from flask import Flask, request, flash, render_template, session, redirect, url_for
from login_form import Register
from sign_in import Sign_In
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = 'development key'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.sqlite3'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    emailId = db.Column(db.String(30))
    passwd = db.Column(db.String(20))
    
class Ta_email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))

@app.route('/')
def basic():
    return render_template('basic.html')
    
@app.route('/register/', methods = ['GET', 'POST'])
def signUp():
    form = Register()
    
    if request.method == 'POST':
        if form.validate == True:
            flash('All fields are required!')
            return render_template('signup.html', form=form)
        else:
                usrnm = request.form['username']
                email = request.form['email']
                password = request.form['password']
                
                user = Users(name=usrnm, emailId=email, passwd=password)
                check_usrnm = user.query.filter_by(name=usrnm).first()
                check_email = user.query.filter_by(emailId=email).first()
                
                if check_usrnm is not None:
                    flash('Username already exists!')
                    return render_template('signup.html', form=form)
                elif check_email is not None:
                    flash('Email already registered!')
                    return render_template('signup.html', form=form)
                else:
                    db.session.add(user)
                    db.session.commit()
                    flash('Registered succesfully')
                    return render_template('signup.html', form=form)
    elif request.method == 'GET':
        return render_template('signup.html', form=form)
    
@app.route('/login/', methods = ['GET', 'POST'])
def signIn():
    form = Sign_In()
    
    if request.method == 'POST':
        if form.validate == True:
            flash('All fields are required!')
            return render_template('sign_in.html', form=form)
        else:
            userId = request.form['userId']
            password = request.form['password']
            user = Users(name=userId, passwd=password)
            check = user.query.filter_by(name=userId, passwd=password).first()
            if check is not None:
                session['username'] = userId
                # if userId == 'admin':
                return render_template('loggedIn.html', user=userId)
            else:
                flash('Invalid Credentials!')
                return render_template('sign_in.html', form=form)
    elif request.method == 'GET':
        return render_template('sign_in.html', form=form)
            
@app.route('/uploader', methods = ['POST', 'GET'])
def upload_file1():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'

@app.route('/logout/')
def logOut():
    session.pop('username', None)
    return redirect(url_for('basic'))

@app.route('/nav/<var>/')
def nav(var):
    return render_template(var)
                
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
