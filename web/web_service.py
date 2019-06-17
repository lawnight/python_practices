from flask import Flask

# http://127.0.0.1/w 访问静态html
app = Flask(__name__,static_folder=r'D:\code\python_practices\html',static_url_path=r'/w')

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5005)


