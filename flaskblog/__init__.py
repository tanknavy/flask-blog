## __init__.py文件表示这是一个package,里面包含Module,
## 包里init文件中可以被外界引用

import os
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
#from flaskblog.forms import RegistrationForm, LoginForm  # 自定义form, 放到最下面，避免循环调用,不需要
#from models import User, Post #DB，循环引用？
from flask_bcrypt import Bcrypt #密码加密
from flask_login import LoginManager # session管理
from flask_mail import Mail


from flaskblog.config import Config

app = Flask(__name__)
#print(app.__name__) #测试
# import secrets
# secrets.token_hex(16)
#app.config['SECRET_KEY'] = 'b4862a51f6c62cb0f1942e79127e069b' # 跨域KeyError: 'A secret key is required to use CSRF.'
# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://hive:q1w2e3r4@spark3:3306/test' #没有+mysqlconnector也可
# 使用配置类
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) # login,logout, current_user
#login_manager.login_view = 'login' #当网页必须要登录时，如果没有登录转到登录页面
login_manager.login_view = 'users.login' #blueprint后当网页必须要登录时，如果没有登录转到登录页面
login_manager.login_message_category = 'info' #当网页需要登录时而没有登录时的信息级别

# 邮箱
# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app)

#from flaskblog.forms import RegistrationForm, LoginForm  # 自定义form，

##################################################
# 路由和表单全部在一个文件中
#初始化文件中中要添加路由，否则主文件中只有app，没有路由！！！
#依旧需要注意循环引用， 所以放到最下面
#from flaskblog import routes


# 使用blueprint后的路由
# routes/forms按业务分开， 使用blueprint延时使用app
from flaskblog.main.routes import main
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.errors.handler import errors

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(errors)

#之前url_for('function')格式，现在全部要改为blueprint格式
# url_for('home') -> url_for('main.home')
# url_for('user_posts') -> url_for('users.user_posts')
# url_for('delete_post') -> url_for('posts.delete_post')


# 可以使用如下函数创建app和绑定环境
# 当前app使用什么配置
# 暂时没有被调用!!
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)


    #db = SQLAlchemy()
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)  # login,logout, current_user
    mail.init_app(app)

    from flaskblog.main.routes import main
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
