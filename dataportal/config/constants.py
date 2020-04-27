import os
import sys


class Constants(object):
    PROJECT_DIR = os.path.dirname(sys.modules['__main__'].__file__)
    FILES_DIR = os.path.dirname(sys.modules['__main__'].__file__) + '/files'
    CONFIG_DIR = os.path.dirname(sys.modules['__main__'].__file__) + '\\config'
    ASSETS_DIR = os.path.dirname(sys.modules['__main__'].__file__) + '\\assets'
    UPLOAD_DIR = ASSETS_DIR+'\\upload'

    STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

    #WEB_URL = "http:\\" + os.environ['SERVER_NAME']

    # ADMIN_MAIL_ADDR = 'testpython1900@gmail.com'
    # ADMIN_MAIL_PASS = 'boldoo1900'

    # note (turn on less secure app from mail account)
    ADMIN_MAIL_ADDR = 'testpython1900@gmail.com'
    ADMIN_MAIL_PASS = 'boldoo1900'

    MAIL_TEMPLATE_FILE = FILES_DIR+'/template_regist.txt'
    ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

    # database configuration
    DB_HOST = '192.168.10.105'
    DB_USER = 'root'
    DB_PASSWORD = ''
    DB_NAME = 'transit'
