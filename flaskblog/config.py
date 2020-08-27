import os
# 配置类
# 类似java接口中使用constant常量

class Config:
    SECRET_KEY = 'b4862a51f6c62cb0f1942e79127e069b'  # 跨域KeyError: 'A secret key is required to use CSRF.'
    # mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://hive:q1w2e3r4@spark3:3306/test'  # 没有+mysqlconnector也可

    # 邮箱
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')