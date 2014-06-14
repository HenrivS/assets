# db_migrate.py  HvS Assets
from views import db
from datetime import datetime
from config import DATABASE_PATH
import sqlite3

with sqlite3.connect(DATABASE_PATH) as connection:
    c=connection.cursor()
    c.execute("""ALTER TABLE HvSAssets RENAME TO old_HvSAssets""")
    db.create_all()
    
    c.execute("""SELECT asset_type, asset_descr, install_date, priority, status FROM old_HvSAssets ORDER BY asset_id ASC""")

# save all rows as a list of tuples; set posted date to now and user id to 1
    data=[(row[0], row[1], row[2], row[3], datetime.now(), 1, 1) for row in c.fetchall()]
    
    # insert data to HvSAssets table
    c.executemany("""INSERT INTO HVSAssets(asset_type, asset_descr, install_date, priority, posted_date, status, user_id) VALUES(?, ?, ?, ?, ?, ?, ?)""", data)
    
    # remove old HvSAssets
    c.execute("DROP TABLE old_HvSAssets")