from flask import Flask, request, send_file

app = Flask(__name__)
app.config.from_object('settings')
app.config.from_envvar('LYDON_SETTINGS')

import os
import boto
from PIL import Image


@app.route('/', methods=['GET',])
def index():
    """Welcome page. Just for kicks. Does absolutely nothing."""
    return '<img src="http://media.digitalphotogallery.com/fvwxvyxzsjud/images/d9ce1e88-eb67-437d-8135-4779a6248cf4/john_lydon01_website_image_dywf_wuxga.jpg" style="height: 500px;" />', 200


@app.route('/<path:source>', methods=['GET',])
def get(source):
    """With no qualifiers, just returns source object... as is."""
    path = _get_source_file(source)
    return _push_file(path)


@app.route('/<path:source>/<int:height>x<int:width>.<format>', methods=['GET',])
def transform(source, width=None, height=None, format='jpg'):
    """Transforms source object per specified qualifiers."""
    im = Image.open(_get_source_file(source))
    im.thumbnail([height, width], Image.ANTIALIAS)

    out_path = os.path.join(get_working_directory(), 'output', source, '%sx%s.%s' % (width, height, format))
    out_dir = os.path.dirname(out_path)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    im.save(out_path)

    return _push_file(out_path)


def _get_source_file(source):
    """Pulls source file from S3 into working directory."""
    s3 = boto.connect_s3(app.config['AWS_ACCESS_KEY_ID'], app.config['AWS_SECRET_ACCESS_KEY'])
    bucket = s3.get_bucket(app.config['AWS_BUCKET'])
    key = bucket.get_key(source)

    local_path = _get_local_file_path(source)
    local_dir = os.path.dirname(local_path)
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    key.get_contents_to_filename(local_path)

    return local_path


def _get_local_file_path(source):
    """Build a file path for local copy of source file."""
    return os.path.join(_get_working_directory(), source)


def _get_working_directory():
    """Build a file path for local copy of source file."""
    return app.config['LYDON_WORKING_DIR']


def _push_file(path):
    """Pushes file stream to browser."""
    return send_file(path, cache_timeout=app.config["LYDON_CACHE_TIMEOUT"])


if __name__ == '__main__':
    app.run()
