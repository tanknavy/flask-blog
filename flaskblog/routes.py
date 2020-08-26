import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm # 自定义form,现在从包中的模块中引用
from flask_login import login_user, current_user, logout_user, login_required
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


# 路由
@app.route("/")
@app.route("/home")  # 让这两个路由指向同一网页
def home():
    # return "<h3>Hello Mr. Millions Cheng</h3>" #返回html语法
    # 使用网页模板渲染，网页在同级的templates目录下
    # Flask使用Jinjia2作为template engine
    return render_template('home.html', posts=blog_list)


@app.route("/about")
def about():
    # return "<h3>about page</h3>"
    return render_template('about.html', title='About')  # 使用网页模板渲染


# 表单处理
@app.route("/register", methods=['GET', 'POST'])  # 初次GET页面，提交表单时POST， form检测validate_on_submit
def register():
    # 如果已经登录认证过了，session还有效
    if current_user.is_authenticated: #在User类中继承了UserMixin
        return redirect(url_for('home'))
    # 如果没有
    form = RegistrationForm()
    # print(form.username.data)
    #print(form.email.data)
    if form.validate_on_submit():  # 校验成功后hash密码
        # 接受表单数据，封装到bean，写入DB
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        #print(form.username.data)
        #flash(f'Account created for {form.username.data}!', 'success') # 快闪信息
        flash(f'Account created in DB for {form.username.data}!', 'success')  # 快闪信息

        #return redirect(url_for('home'))  # 成功就重定向到主页
        return redirect(url_for('login'))  # 成功就重定向到主页
    return render_template('register.html', title='Register', form=form) # 模板中使用form


@app.route("/login", methods=['GET', 'POST'])
def login():
    # 如果已经登录认证过了，session还有效
    if current_user.is_authenticated: #在User类中继承了UserMixin
        return redirect(url_for('home'))
    # 如果没有
    form = LoginForm()
    if form.validate_on_submit():
        # 登录校验
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):# 用户存在且密码匹配
            #print('user and password match!')
            login_user(user, remember=form.remember.data) #
            # 网页需要登录才能访问，如果没有则引导登录，next_page将是登录后要跳转的网页
            next_page = request.args.get('next') # 请求的next参数
            print(next_page)
            return redirect(next_page) if next_page else redirect(url_for('home')) #需要返回
        else:
            flash('Login failed, please check email and password', 'danger')
        # #非DB测试
        # if form.email.data == 'cheng_alex@126.com' and form.password.data == 'ac32':
        #     flash(f'You have benn logged in!', 'success')  # 快闪信息
        #     return redirect(url_for('home'))
        # else:
        #     flash('Login failed, please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)  # 使用网页模板渲染


@app.route("/logout")
def logout():
    logout_user() #登出当前用户，网页中已经判断用户已经登录，会出现logout按钮
    #return redirect(url_for('about'))
    return redirect(url_for('home'))



def save_picture(form_picture): #传入一个图片文件对象
    random_hex = secrets.token_hex(8) #文件新命名
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_name) #文件路径
    #form_picture.save(picture_path)  # 保存路径
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size) #图片剪裁
    i.save(picture_path) #保存路径

    return picture_name #返回新文件名


@app.route("/account", methods=['GET','POST'])
@login_required #装饰器，必须登录验证过，才能正常展示如下内容
def account():
    form = UpdateAccountForm() #修改用username和email
    if form.validate_on_submit(): #提交用户名和信息
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.picture.data: #更新图片
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file #保存的文件名
        ##current_user.password = form.username.data #注意:current_user绑定了现在用户的表，会提交更新user的相关内容
        db.session.commit() # 提交更新,这里怎么知道提交到哪个class
        flash('your account is updated!', 'success')
        return redirect(url_for('account')) #不使用render_template
    elif request.method == 'GET': #已经登录了，当前是查看状态
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)  # 使用网页模板渲染