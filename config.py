import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    """
        Set Config variables for the flask app.
        Using Environment variables where available otherwise
        create the config variable if not done already.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Turn off update messages from the sqlalchemy