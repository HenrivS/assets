# config.py HvS Assets app
import os

# grabs the folder where the scripts run
basedir=os.path.abspath(os.path.dirname(__file__))

DATABASE='HvSAssets.db'
SECRET_KEY='my_precious'

# defines the full path for the database
DATABASE_PATH=os.path.join(basedir, DATABASE)

#the database uri
SQLALCHEMY_DATABASE_URI='sqlite:///' + DATABASE_PATH