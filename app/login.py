#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 22:20:36 2020

@author: sanjay
"""

from flask import Flask, request, flash, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from forms import Register, Sign_In, change_password
from flask_sqlalchemy import SQLAlchemy
from io import TextIOWrapper
import csv

app = Flask(__name__)   

app.secret_key = 'development key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3'

db = SQLAlchemy(app)

# from models import Users, ta_email, admin

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
                password = generate_password_hash(password)
                email_exists = ta_email.query.filter_by(email=email).first()
                if email_exists is None:
                    flash('You are not authorised to signup ):')
                    return render_template('signup.html', form=form, flag=0)
                else:
                    user = Users(name=usrnm, email=email, password=password)
                    check_usrnm = user.query.filter_by(name=usrnm).first()
                    check_email = user.query.filter_by(email=email).first()

                    if check_usrnm is not None:
                        flash('Username already exists!')
                        return render_template('signup.html', form=form, flag=0)
                    elif check_email is not None:
                        flash('Email already registered!')
                        return render_template('signup.html', form=form, flag=0)
                    else:
                        db.session.add(user)
                        db.session.commit()
                        flash('Registered succesfully!')
                        return render_template('signup.html', form=form, flag=1)
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
                user = admin.query.filter_by(name = userId).first()
            elif whichUser == 'T':
                user = Users.query.filter_by(name = userId).first()
            else:
                flash('Invalid Credentials!')
                return render_template('sign_in.html', form=form)
            val1 = (userId == 'admin' and password == 'admin@iitk')
            val2 = (userId == 'manager' and password == 'manager@iitk')
            val = val1 or val2
            if val or (user and check_password_hash(user.password, password)):
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
        return render_template(userId +'.html', user=session["username"], flag=1)
    return render_template('ta.html', user=session['username'])

@app.route('/upload-ta', methods=['GET', 'POST'])
def upload_csv():
    if session['username'] == None:
        flash('You are logged out!')
        return render_template('basic.html')
    if request.method == 'POST':
        csv_file = request.files['file']
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            user = ta_email(email=row[1])
            db.session.add(user)
            db.session.commit()
        flash('file uploaded succesfully')
        return render_template('admin.html', user=session['username'], flag=1)
    return render_template('ta-details.html', user=session["username"])

@app.route('/change-password', methods = ['GET', 'POST'])
def changePassword():
    if session['username'] == None:
        flash('You are logged out!')
        return render_template('basic.html')
    form = change_password()
    if request.method == 'POST':
        if form.validate == True:
            flash('Please enter all fields')
        else:
            username = session['username']
            if username == 'admin' or username == 'manager':
                user = admin.query.filter_by(name = username).first()
            else:
                user = Users.query.filter_by(name = username).first()

            new_password = request.form['password']
            confirm = request.form['confirm']

            if new_password != confirm:
                flash('Password Mismatch')
                return render_template('change_password.html', form=form, user=username, flag=0)
            elif check_password_hash(user.password, new_password):
                flash('Please enter a new password')
                return render_template('change_password.html', form=form, user=username, flag=0)
            else:
                session['password'] = new_password
                user.password = generate_password_hash(new_password)
                db.session.commit()
                flash('Password changed succesfully!')
                return render_template('change_password.html', user=session['username'], form=form, flag=1)
    elif request.method == 'GET':
        return render_template('change_password.html', form=form, user=session['username'])

@app.route('/see-emails')
def see_emails():
    if session['username'] == None:
        flash('You are logged out!')
        return render_template('basic.html')
    return render_template('admin.html', user=session['username'], users=ta_email.query.all(), show_table=1)

if __name__ == '__main__':
    from models import Users, admin, ta_email
    db.create_all()
    app.run(debug=True)
