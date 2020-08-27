
from flaskblog import app, create_app

#app = create_app() #当使用create_app时，其它直接调用app的先使用current_app，
# 如果不想设置环境变量set FLASK_DEBUG=1,可以这样
# __main__, 如果直接运行，__name__就等于__main__, 在别的module中导入时不会
if __name__ == '__main__':
    app.run(debug=True)
