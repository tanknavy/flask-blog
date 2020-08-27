#from flaskblog import db #一个已经绑定了app的alchemy实例对象，可以操作DB
# 除了使用__main__这样，最好是使用package来包装相关模块
#from __main__ import db # 因为引用的是实例对象需要runtime的？其实这时flaskblog.py名字是main了， 注意循环引用circular import
from flaskblog import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# 用户authentication
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 类似bean
#class User(db.Model): #多继承，用户验证，UserMinxin用于用户验证
# 如果没有UserMixin, 就会'User' object has no attribute 'is_authenticated'
class User(db.Model, UserMixin): #多继承，用户验证，UserMinxin用于用户数据的处理
    id = db.Column(db.Integer, primary_key=True) #主键
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') #长度？
    password = db.Column(db.String(60), nullable=False) # hash加密成60位长

    # one-to-many关系，不是一个db栏位，方便通过该用户查到他全部的post
    # user.posts拿到全部post, post.author拿到用户信息
    posts = db.relationship('Post', backref='author', lazy=True)

    # 加入session/token过期
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec) #传入secret_key，设定1800秒过期
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod #静态方法，工具方法
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None #用户token过期
        return User.query.get(user_id) #没有过期就去查用户名

    def __repr__(self): #方便查看
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #这里utcnow后面无需()
    content = db.Column(db.Text, nullable=False)

    # user到post的one-to-many关系，外键约束， MUL标识，外键中写的是表的栏位，不是类的字段
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #这里外键user.id是因为参考表user小写的，不是类

    def __repr__(self): #方便查看
        return f"Post('{self.title}', '{self.date_posted}')"