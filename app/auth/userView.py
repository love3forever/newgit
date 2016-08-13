#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-11 15:20:21
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from flask import redirect, url_for, request, render_template, flash
from flask.ext.login import login_user, logout_user, current_user
from . import auth
from ..models import User
from authforms import LoginForm, RegisterForm


@auth.route('/reset_password')
def password_reset_request():
    pass

@auth.route('/reset_email')
def email_reset_request():
    pass


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data, password=form.password.data)
        user.save()
        return redirect(url_for('main.main_index'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.rememberme.data)
            return render_template('index.html')
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

