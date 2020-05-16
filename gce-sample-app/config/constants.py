import os
import sys

class Constants(object):
    SQL_DDL = os.path.dirname(sys.modules['__main__'].__file__) + '/docker/sql/ddl.sql'
    CSV_CONVERSION = os.path.dirname(sys.modules['__main__'].__file__) + '/docker/sql/cv_log.csv'
    CSV_PURCHASE = os.path.dirname(sys.modules['__main__'].__file__) + '/docker/sql/purchase_log.csv'

    # database configuration
    # DB_USER = os.environ.get("root")
    # DB_PASSWORD = os.environ.get("kasemituyo3")
    # DB_NAME = os.environ.get("app_reports")
    # CONN_NAME = os.environ.get("gj-bootcamp2020:asia-east2:bootcamp2020")
    CONN_CLOUD = 'gj-bootcamp2020:asia-east2:bootcamp2020'
    DB_HOST = '127.0.0.1'
    DB_USER = 'test'
    DB_PASSWORD = '123'
    DB_NAME = 'app_reports'
