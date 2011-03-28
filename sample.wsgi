import os
import sys

sys.stdout = sys.stderr

activate_this = 'PATH_TO_VIRTUALENV/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, 'PATH_TO_YOUR_PROJECT')
os.environ['LYDON_SETTINGS'] = 'YOUR_SETTINGS_MODULE'

from lydon import app as application