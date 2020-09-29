from flask import Flask
from flask_assets import Environment, Bundle

# http://127.0.0.1/w 访问静态html
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    
    app.run(host='0.0.0.0',port=5005)
    assets = Environment(app)

    # assets.register('js',)