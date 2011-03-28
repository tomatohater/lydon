from flask import Flask, request, send_file

app = Flask(__name__)
app.config.from_object('settings')
app.config.from_envvar('LYDON_SETTINGS')

import os
import boto
from PIL import Image


@app.route('/lydon/<path:source>/<int:height>x<int:width>.<format>', methods=['GET',])
def transform(source, height=None, width=None, format='jpg'):
    im = Image.open(get_source_file(source))
    im.thumbnail([height, width], Image.ANTIALIAS)
    
    out = os.path.join(get_working_directory(), 'output', source)
    im.save(out) 

    return send_file(out)

def get_source_file(source):
    s3 = boto.connect_s3(app.config['AWS_ACCESS_KEY_ID'], app.config['AWS_SECRET_ACCESS_KEY'])
    bucket = s3.get_bucket(app.config['AWS_BUCKET'])
    key = bucket.get_key(source)
    
    local_path = get_local_file_path(source)
    key.get_contents_to_filename(local_path)
    
    return local_path

def get_local_file_path(source):
    return os.path.join(get_working_directory(), source)

def get_working_directory():
    return app.config['LYDON_WORKING_DIR']



if __name__ == '__main__':
    app.run()
