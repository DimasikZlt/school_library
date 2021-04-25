"""Flask configuration."""
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(basedir, 'db', 'library.sqlite')
db_type = 'sqlite:///'

SQLALCHEMY_DATABASE_URI = f"{db_type}{db_dir}"
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = True
SECRET_KEY = "my_secret_key_I_won't_say"
