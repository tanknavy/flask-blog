import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

# 可使用current_app替代
from flaskblog import app


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


def send_reset_email(user):
    token = user.get_reset_token()  # 1800秒过期的token
    msg = Message('Password Reset Request', sender='noreply@gmail.com', recipients=[user.email])
    # 重置密码的链接，外部使用
    msg.body = f'''To reset your password, visit the following link:
        {url_for('reset_token', token=token, _external=True)}

        If you did not make this request, please ignore   
    '''
    # mail.send(msg) #发送邮件

