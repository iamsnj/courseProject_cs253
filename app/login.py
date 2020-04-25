#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 22:20:36 2020

@author: sanjay
"""


from flask import Flask, request, flash, render_template, session, redirect, url_for
from forms import Register, Sign_In, change_password
from flask_sqlalchemy import SQLAlchemy
from io import TextIOWrapper
import csv

app = Flask(__name__)   

app.secret_key = 'development key'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(40))
    password = db.Column(db.String(20))
    
class ta_email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40))

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(40))
    password = db.Column(db.String(20))

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
                email_exists = ta_email.query.filter_by(email=email).first()
                if email_exists is None:
                    flash('You are not authorised to signup ):')
                    return render_template('signup.html', form=form)
                else:
                    user = Users(name=usrnm, email=email, password=password)
    
                    check_usrnm = user.query.filter_by(name=usrnm).first()
                    check_email = user.query.filter_by(email=email).first()
                    
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
            whichUser = request.form['whichUser']
            if whichUser == 'A':
                user = admin(name=userId, password=password)
            elif whichUser == 'T':
                user = Users(name=userId, password=password)
            else:
                flash('Invalid Credentials!')
                return render_template('sign_in.html', form=form)
            check = user.query.filter_by(name=userId, password=password).first()
            if check is not None:
                session['username'] = userId
                session['password'] = password
                return redirect(url_for('login_users'))
            else:
                flash('Invalid Credentials!')
                return render_template('sign_in.html', form=form)
    elif request.method == 'GET':
        return render_template('sign_in.html', form=form)

@app.route('/logout/')
def logOut():
    session.pop('username', None)
    session.pop('password', None)
    session['username'] = None
    return redirect(url_for('basic'))

@app.route('/user')
def login_users():
    if session['username'] == None:
        flash('You are logged out!')
        return render_template('basic.html')
    userId = session['username']
    if userId == 'admin' or userId == 'manager':
        return render_template('admin.html', user=session["username"])
    return session['username']

@app.route('/ta-details')
def ta_details():
    if session['username'] == None:
        flash('You are logged out!')
        return render_template('basic.html')
    return render_template('ta-details.html', user=session['username'])

@app.route('/upload-ta', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        csv_file = request.files['file']
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            user = ta_email(email=row[1])
            db.session.add(user)
            db.session.commit()
        flash('file uploaded succesfully')
        return render_template('ta-details.html', user=session['username'])
    return render_template('upload.html', user=session["username"])

@app.route('/change-password', methods = ['GET', 'POST'])
def changePassword():
    if session['username'] == None:
        flash('You are logged out!')
        return render_template('basic.html')
    form = change_password()
    if request.method == 'POST':
        if form.validate == True:
            flash('Please enter a password')
        else:
            old_password = session['password']
            new_password = request.form['password']
            confirm = request.form['confirm']
            if new_password != confirm:
                flash('Password Mismatch')
                return render_template('change_password.html', form=form, user=session['username'])
            if old_password == new_password:
                flash('Please enter a new password')
                return render_template('change_password.html', form=form, user=session['username'])
            else:
                session['password'] = new_password
                if session['username'] == 'admin' or session['username'] == 'manager':
                    user = admin.query.filter_by(name=session['username']).first()
                    user.password = new_password
                else:
                    user = Users.query.filter_by(name=session['username']).first()
                    user.password = new_password
                db.session.commit()
                flash('Password changed succesfully!')
                return render_template('change_password.html', user=session['username'], form=form)
    elif request.method == 'GET':
        return render_template('change_password.html', form=form, user=session['username'])
    

@app.route('/remove-ta')
def remove_ta():
    return render_template('ta-details.html', user=session['username'])

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
