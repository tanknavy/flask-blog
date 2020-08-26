
from flaskblog import app

# 如果不想设置环境变量set FLASK_DEBUG=1,可以这样
# __main__, 如果直接运行，__name__就等于__main__, 如果在别的module中导入使用就不会
if __name__ == '__main__':
    app.run(debug=True)
