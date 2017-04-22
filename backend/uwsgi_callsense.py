import sys
import os

APP_PATH = '/var/www/callsense'
sys.path.insert(0, APP_PATH)
os.chdir(APP_PATH)

from api import app as application
