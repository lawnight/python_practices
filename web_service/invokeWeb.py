import requests
import os
import web


siPath = '/Users/near/work/war_mix_server/si'

startUrl = 'http://127.0.0.1:5000/start'


if __name__ == '__main__':   
    # web.upload(siPath,web.postUrl)
    web.savePath = './'
    web.app.run()

    requests.get(startUrl)