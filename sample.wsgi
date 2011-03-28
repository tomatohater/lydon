import os
import sys

sys.path.insert(0, 'PATH_TO_YOUR_PROJECT')
sys.path.insert(0, 'PATH_TO_VIRTUALENV_SITEPACKAGES')

os.environ['LYDON_SETTINGS'] = 'YOUR_SETTINGS_MODULE'

from lydon import app as application
