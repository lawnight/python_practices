# -*- coding: utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory
import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


savePath ='/Users/near/Library/Python'

postUrl = 'http://127.0.0.1:5000'

#向服务器上传文件
def upload(path,url):
    for item in os.listdir(path):
        file_path = os.path.join(path, item)
        if os.path.isdir(file_path):
            upload(file_path,url)
        else:            
            with open(file_path, 'rb') as the_file:
                files = {'file': the_file}        
                response = requests.post(url,files=files)

# 服务器接受上传文件
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']       
        file.save(os.path.join(savePath,file.filename))
        print 'save file:' + file.filename
    return ""

@app.route('/start')
def start():
    print('hello start!')
    # path = 'G:\100day\br_cn_tools\si服务器生成'

    # os.system(os.path.join(path,'si.bat'))
    # upload(os.path.join(path,'java','com'),postUrl)
    # upload(os.path.join(path,'java','server'),postUrl)
    return ""
    #copy file
   
    

@app.route("/download")
def downloader():
    dirpath = os.path.join(app.root_path, 'upload')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
    return send_from_directory(dirpath, filename, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载


if __name__ == '__main__':
    app.run()