import os
from flask import Flask, render_template, redirect, request
from flaskblog.models import Post
from flask import Blueprint

#蓝图，route和app的集合，延时需要app
# 比如这里的@app.route, 现在统一改为posts.route()
main = Blueprint('main', __name__)


# 主页路由
@main.route("/")
@main.route("/home")  # 让这两个路由指向同一网页
def home():
    # return "<h3>Hello Mr. Millions Cheng</h3>" #返回html语法
    # 使用网页模板渲染，网页在同级的templates目录下
    # Flask使用Jinjia2作为template engine
    # 全部查询
    #posts = Post.query.all()
    # 使用分页
    # ?page=2可选参数查看第二页
    page = request.args.get('page', 1, type=int) #自定义第几页输出，默认1
    # 全部查询，按照时间栏位倒序排列
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2) #post是一个paginate对象了，html也要更新
    #   {% for post in posts.items %}
    # 使用?page=2
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    # return "<h3>about page</h3>"
    return render_template('about.html', title='About')  # 使用网页模板渲染
