from flask import Blueprint

from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
#from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm  # 自定义form,现在从包中的模块中引用
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm
from flaskblog.models import User, Post
from flaskblog.users.utiles import save_picture, send_reset_email

#蓝图，
# @app.route改为@users.route


users = Blueprint('users', __name__)

# 表单处理
@users.route("/register", methods=['GET', 'POST'])  # 初次GET页面，提交表单时POST， form检测validate_on_submit
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


@users.route("/login", methods=['GET', 'POST'])
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
            return redirect(next_page) if next_page else redirect(url_for('main.home')) #需要返回
        else:
            flash('Login failed, please check email and password', 'danger')
        # #非DB测试
        # if form.email.data == 'cheng_alex@126.com' and form.password.data == 'ac32':
        #     flash(f'You have benn logged in!', 'success')  # 快闪信息
        #     return redirect(url_for('home'))
        # else:
        #     flash('Login failed, please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)  # 使用网页模板渲染


@users.route("/logout")
def logout():
    logout_user() #登出当前用户，网页中已经判断用户已经登录，会出现logout按钮
    #return redirect(url_for('about'))
    return redirect(url_for('home'))

@users.route("/account", methods=['GET','POST'])
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


@users.route("/user/<string:username>")  # 让这两个路由指向同一网页
def user_posts(username):
    #posts = Post.query.all()
    # 使用分页
    # ?page=2可选参数查看第二页
    page = request.args.get('page', 1, type=int) #自定义第几页输出，默认1
    user = User.query.filter_by(username=username).first_or_404()
    # 全部查询，按照时间栏位倒序排列
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=2) #post是一个paginate对象了，html也要更新
    #   {% for post in posts.items %}
    # 使用?page=2
    return render_template('user_posts.html', posts=posts, user=user)


# 先验证邮箱，再重置密码
@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
    # 如果已经登录认证过了，session还有效
    if current_user.is_authenticated:  # 在User类中继承了UserMixin
        return redirect(url_for('home'))

    form = RequestResetForm()
    if form.validate_on_submit():# 开始重置密码
        user = User.query.filter_by(email=form.email.data).first()
        # 发送重置密码的邮件
        send_reset_email(user)
        flash('An email has benn sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title='Reset Pasword', form=form)


@users.route("/reset_password/<token>", methods=['GET','POST']) #无需指定token的类型
def reset_token(token):
    if current_user.is_authenticated:  # 在User类中继承了UserMixin
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if user is None: #token无效
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))

    form = RequestResetForm()
    if form.validate_on_submit():  # 校验成功后hash密码
        # 接受表单数据，封装到bean，写入DB
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #db.session.add(user) #更新操作，无需创建记录
        user.password = hashed_password #要更新的值
        db.session.commit()
        flash(f'Your password has been updated {user}!', 'success')  # 快闪信息
        return redirect(url_for('login'))  # 成功就重定向到主页

    # get方法
    return render_template('reset_token.html', title='Reset Password', form=form)