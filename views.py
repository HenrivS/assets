#views.py  HvS asset app
from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from forms import AddAsset, RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError

app=Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import HvSAssets, User

def login_required(test):
    @wraps(test)
    def wrap (*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("you need to lgin first")
            return redirect (url_for('login'))
    return wrap

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You are logged out')
    return redirect(url_for('login'))

@app.route ('/', methods=['GET', 'POST'])
def login():
    error=None
    if request.method=='POST':
        u=User.query.filter_by(name=request.form['name'],
                               password=request.form['password']).first()
        if u is None:
            error='Invalid username or password'
        else:
            session['logged_in']=True
            session['user_id']=u.id
            flash('You are logged in')
            return redirect(url_for('assets'))
    return render_template("login.html",
                           form=LoginForm(request.form),
                           error=error)

@app.route ('/assets/')
@login_required
def assets():
    open_assets = db.session.query(HvSAssets).filter_by(status="1").order_by(HvSAssets.install_date.asc())
    closed_assets = db.session.query(HvSAssets).filter_by(status="0").order_by(HvSAssets.install_date.asc())
    
    return render_template('assets.html', form=AddAsset(request.form), open_assets=open_assets, closed_assets=closed_assets)

#@app.route ('/display/<int:asset_id>/',)
#def display(asset_id):
#    g.db=connect_db()
#    curr=g.db.execute('select asset_type, asset_descr, install_date, priority, status, asset_id from assets where asset_id='+str(asset_id))
#    display_assets=[dict(type=row[0], descr=row[1], date=row[2], priority=row[3], status=row[4], asset_id=row[5]) for row in curr.fetchall()]    
#    g.db.close()
#    return "ok"
#    return render_template('dash2.html', display_assets=display_assets)



#@app.route ('/dash/')
#@login_required
#def dash():
#    g.db=connect_db()
#    curr=g.db.execute('select asset_type, asset_descr, install_date, priority, status, asset_id from assets where status=1')
#    open_assets = [dict(type=row[0], descr=row[1], date=row[2], priority=row[3], status=row[4], asset_id=row[5]) for row in curr.fetchall()]
#    curr=g.db.execute('select asset_type, asset_descr, install_date, priority, status, asset_id from assets where asset_id="19"')
#    closed_assets=[dict(type=row[0], descr=row[1], date=row[2], priority=row[3], status=row[4], asset_id=row[5]) for row in curr.fetchall()]    
#    g.db.close()
#    return render_template('dash.html', open_assets=open_assets, display_assets=closed_assets)


#add assets
@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_asset():
    
    form=AddAsset(request.form, csrf_enabled=False)
    
    if form.validate_on_submit():
#        return(form.asset_type.data)
#    else:
#        return "not validated"
        new_asset=HvSAssets(
                            form.asset_type.data,
                           form.asset_descr.data,
                           form.install_date.data,
                           form.priority.data,
                           form.posted_date.data,
                           '1',
                           session['user_id']
                           )
        
        db.session.add (new_asset)
        db.session.commit()
        flash('New entry successfully posted')
    else:
        flash_errors(form)
    return redirect(url_for('assets'))

#change asset status
@app.route('/complete/<int:asset_id>/',)
@login_required
def complete(asset_id):
    new_id=asset_id
    db.session.query(HvSAssets).filter_by(asset_id=new_id).update({"status":"0"})
    db.session.commit()
    flash('The asset status was changed')
    return redirect (url_for('assets'))

#display asset detail
#@app.route('/display/<int:asset_id>/',)
#@login_required
#def display(asset_id):
#    g.db=connect_db()
#    curr=g.db.execute('select asset_type, asset_descr, install_date, priority, status, asset_id from assets where asset_id='+str(asset_id))
#    display_assets=[dict(type=row[0], descr=row[1], date=row[2], priority=row[3], status=row[4], asset_id=row[5]) for row in curr.fetchall()]
#   g.db.close()
#   flash('The asset status was changed')
#    return redirect (url_for('display', assets=display_assets))





#Delete asset
@app.route('/delete/<int:asset_id>/',)
@login_required
def delete_asset(asset_id):
    new_id=asset_id
    db.session.query(HvSAssets).filter_by(asset_id=new_id).delete()
    db.session.commit()
    flash('the asset was deleted')
    return redirect (url_for('assets'))

@app.route ('/register/', methods=['GET', 'POST'])
def register():
    error= None
    form=RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():

        new_user=User(
                      form.name.data,
                      form.email.data,
                      form.password.data,
                      )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Thank you for registering. Please login')
            return redirect(url_for ('login'))
        except IntegrityError:
            error='That username and/or email already exists -- Please try again'
            return render_template('register.html', form=form, error=error)
    else:
        flash_errors(form)
        return render_template('register.html', form=form, error=error)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash (u"Error in the %s field -%s" %(
            getattr(form,field).label.text,error), 'error')

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template ('500.html'), 500

@app.errorhandler(404)
def internal_error(error):
    return render_template ('404.html'), 404

       