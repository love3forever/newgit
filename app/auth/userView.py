#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-11 15:20:21
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from flask import redirect, url_for, request, render_template, flash, g, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from . import auth
from ..models import User
from authforms import LoginForm, RegisterForm, ResetPasswordForm, ResetEmailForm


@auth.before_app_request
def before_request():
    pass


@auth.route('/reset_password', methods=['GET', 'POST'])
@login_required
def password_reset_request():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if form.oldpsw.data == current_user.password:
            current_user.password = form.newpsw.data
            current_user.save()
            logout_user()
            flash('Password changed! Please Login in')
            return render_template('index.html')
        flash('Invalid password.')
    return render_template('auth/resetpsw.html', form=form)


@auth.route('/reset_email', methods=['GET', 'POST'])
@login_required
def email_reset_request():
    form = ResetEmailForm()
    if form.validate_on_submit():
        if form.oldemil.data == current_user.email:
            current_user.email = form.newemail.data
            current_user.save()
            flash('Email changed!')
            return redirect(url_for('main.main_index'))
        flash('Invalid email')
    return render_template('auth/resetemil.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data, password=form.password.data)
        user.save()
        login_user(user)
        return redirect(url_for('main.main_index'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        next = request.args.get('next')
        if next:
            return redirect(next)
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.objects(username=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                login_user(user, form.rememberme.data)
                return render_template('index.html', current_user=user)
            flash('Invalid username or password.')
        return render_template('auth/login.html', form=form)
