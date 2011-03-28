from flask import Flask, request

app = Flask(__name__)
app.config.from_object('lydon.settings')
app.config.from_envvar('LYDON_SETTINGS')


import boto
from PIL import Image

#HxW-flags.ext
#@app.route('/post/<int:post_id>')

@app.route('/lydon/<path:source>/<int:height>x<int:width>.<format>', methods=['GET',])
def transform(source, height=None, width=None, format='jpg'):
    




if __name__ == '__main__':
    app.run()
