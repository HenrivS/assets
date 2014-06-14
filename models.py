#models.py  HvS Assets
from views import db

class HvSAssets(db.Model):
    __tablename__="HvSAssets"
    asset_id=db.Column(db.Integer, primary_key=True)
    asset_type=db.Column(db.String, nullable=False)
    asset_descr=db.Column(db.String, nullable=False)
    install_date=db.Column(db.Date, nullable=False)
    priority=db.Column(db.Integer, nullable=False)
    posted_date=db.Column(db.Date, nullable=False)
    status=db.Column(db.Integer)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __init__(self,asset_type,asset_descr,install_date,priority, posted_date, status, user_id):
        self.asset_type=asset_type
        self.asset_descr=asset_descr
        self.install_date=install_date
        self.priority=priority
        self.posted_date=posted_date
        self.status=status
        self.user_id=user_id    
    
    def __repr__ (self):
        return'<name %r>' %self.body

class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, unique=True, nullable=False)
    email=db.Column(db.String, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    assets=db.relationship('HvSAssets', backref=('poster'))
    
    def __init__ (self, name=None, email=None, password=None):
        self.name=name
        self.email=email
        self.password=password
    
    def __repr__(self):
        return '<user %r>' %self.name
    
        
     