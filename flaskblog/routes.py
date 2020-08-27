# import os
# import secrets
# from PIL import Image
# from flask import Flask, render_template, url_for, flash, redirect, request, abort
# from flaskblog import app, db, bcrypt, mail
# from flaskblog.models import User, Post
# from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm # 自定义form,现在从包中的模块中引用
# from flask_login import login_user, current_user, logout_user, login_required
# from flask_mail import Message
#-----------上述引用全部放到项目同名的包下面的__init__.py文件中

# 为了避免和models的循环引用,因为models中有import db
# 先有这里的db对象，models中才能产生User，Product类
# db可以建表，CRUD

# 一个user写多个post, one-to-many


# snippet样式
# https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog/snippets
# git
# https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog

# 模拟静态数据
blog_list = [
    {
        'author': 'Alex Cheng',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2020'
    },
    {
        'author': 'Bob Cheng',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2020'
    }
]





















