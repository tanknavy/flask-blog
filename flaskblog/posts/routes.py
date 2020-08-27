from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required

from flaskblog import db
#from flaskblog.forms import PostForm  # 自定义form,现在从包中的模块中引用
from flaskblog.posts.forms import PostForm
from flaskblog.models import Post

#蓝图，route和app的集合，延时创建, 必须在package中
# 比如这里的@app.route, 现在统一改为posts.route()
posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been create!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')  # 使用网页模板渲染


# 单帖子显示
@posts.route("/post/<int:post_id>") #注意<>中不能有空格
def post(post_id):
    post = Post.query.get_or_404(post_id) # 存在或者返回404
    return render_template('post.html', title='Post', post=post)  # 使用网页模板渲染


# 更新帖子
@posts.route("/post/<int:post_id>/update", methods=['GET','POST']) #注意<>中不能有空格
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) #数据model
    #只能修改自己的帖子
    if post.author != current_user:
        abort(403)
    form = PostForm() #view视图
    # 更新已有的帖子
    if form.validate_on_submit(): # POST
        post.title = form.title.data
        post.content = form.content.data
        #db.session.add(post) #这里无需创建post，因为post已经存在并且读出
        db.session.commit() #提交更新
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id)) #返回更新后的帖子
    elif request.method == 'GET': #展示
        #修改前默认先展示要修改的帖子
        form.title.data = post.title #读取现有数据
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', post=post, form=form, legend='Update Post')  # 使用网页模板渲染


# 删除帖子
@posts.route("/post/<int:post_id>/delete", methods=['POST']) #提交删除请求
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # 数据model
    # 只能修改自己的帖子，如果不是自己的帖子网页中按钮也会隐藏
    if post.author != current_user:
        abort(403) # 权限不足
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


