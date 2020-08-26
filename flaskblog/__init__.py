## __init__.py文件表示这是一个package,里面包含Module,
## 包里init文件中可以被外界引用

from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
#from flaskblog.forms import RegistrationForm, LoginForm  # 自定义form, 放到最下面，避免循环调用,不需要
#from models import User, Post #DB，循环引用？
from flask_bcrypt import Bcrypt #密码加密
from flask_login import LoginManager # session管理

app = Flask(__name__)
# import secrets
# secrets.token_hex(16)
app.config['SECRET_KEY'] = 'b4862a51f6c62cb0f1942e79127e069b' # 跨域KeyError: 'A secret key is required to use CSRF.'
# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://hive:q1w2e3r4@spark3:3306/test' #没有+mysqlconnector也可
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) # login,logout, current_user
login_manager.login_view = 'login' #当网页必须要登录时，如果没有登录转到登录页面
login_manager.login_message_category = 'info' #当网页需要登录时而没有登录时的信息级别

#from flaskblog.forms import RegistrationForm, LoginForm  # 自定义form，

#初始化文件中中要添加路由，否则主文件中只有app，没有路由！！！
#依旧需要注意循环引用， 所以放到最下面
from flaskblog import routes