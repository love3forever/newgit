#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-11 15:20:21
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from flask import redirect, url_for, request, render_template, flash
from flask.ext.login import login_user, current_user
from . import auth
from ..models import User, Post
from authforms import LoginForm, RegisterForm


@auth.before_app_request
def before_request():
    pass


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
                posts = []
                for post in Post.objects(user=current_user.id):
                    posts.append(post)
                return redirect(url_for('main.main_index', posts=posts))
                # return render_template('index.html', current_user=user)
            flash('Invalid username or password.')
        return render_template('auth/login.html', form=form)
