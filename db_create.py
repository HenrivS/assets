#db_create.py  creates HvS Assets database
from views import db
from models import HvSAssets
from datetime import date

# create the db and table
db.create_all()

#insert data
db.session.add(HvSAssets("type 1", "Green model", date(2014,3,13), 3, 1))
db.session.add(HvSAssets("type 2", "red model", date(2014,3,23), 3, 1))
db.session.add(HvSAssets("type 3", "blue model", date(2014,3,14), 3, 1))    

db.session.commit()