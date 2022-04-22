from flask.globals import request
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from database import User, Review
from sqlalchemy.orm import scoped_session
from utils import *
from textblob import TextBlob
import plotly.express as px
import plotly
import json
import pandas as pd

from flask import  Flask, request,session,flash,redirect,render_template,url_for

app = Flask(__name__)
app.secret_key = "the basics of life with python"

def get_db():
    engine = create_engine('sqlite:///db.sqlite3')
    Session = scoped_session(sessionmaker(bind=engine))
    return Session()

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and validate_email(email):
            if password and len(password)>=6:
                try:
                    sess = get_db()
                    user = sess.query(User).filter_by(email=email,password=password).first()
                    if user:
                        session['isauth'] = True
                        session['email'] = user.email
                        session['id'] = user.id
                        session['name'] = user.name
                        del sess
                        flash('login successfull','success')
                        return redirect('/home')
                    else:
                        flash('email or password is wrong','danger')
                except Exception as e:
                    flash(e,'danger')
            else:
                flash('Password is invalid','danger')
        else:
            flash("email is invalid",'danger')
    print(session)
    if session.get('isauth',False):
        return redirect('/home')
    return render_template('index.html',title='login')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        if name and len(name) >=3:
            if email and validate_email(email):
                if password and len(password)>=6:
                    if cpassword and cpassword == password:
                        try:
                            sess = get_db()
                            newuser = User(name=name,email=email,password= password)
                            sess.add(newuser)
                            sess.commit() 
                            flash('registration successful','success')
                            return redirect('/')
                        except:
                                 flash('email account already exists','danger')
                    else:
                        flash('confirm _PasswordType does not match','danger')
                else:
                    flash('_PassWordType must be of 6 or more characters','danger')
            else:
                 flash('invalid email or ','danger')
        else:
            flash('invalid name, must be 3 or more characters ','danger')
    return render_template('signup.html',title='register')

@app.route('/forgot',methods=['GET','POST'])
def forgot():
    return render_template('forgot.html',title='forgot password')


@app.route('/home',methods=['GET','POST'])
def home():
    appname=None
    if not session.get('isauth',False):
        return redirect('/')
    db = get_db()
    fig1 = None
    if request.method == "POST":
        appname = request.form.get('appname')
        reviews = db.query(Review).filter(Review.app==appname).all()
        db.close()    
    else:
        reviews = db.query(Review).all()[:1000]
    apps = db.query(Review, func.sum(Review.score)).group_by(Review.app).all()
    db.close()
    return render_template('home.html',title='home', reviewlist=reviews,appscore=apps,appname=appname,fig1=fig1)

@app.route('/callback', methods=['GET','POST'])
def cb():
    data =  request.form
    appname = data.get('appname')
    pol = data.get('pol')
    subject = data.get('subject')
    sentiment = data.get('sentiment')
    db = get_db()
    rdf = pd.read_sql(db.query(Review).filter(Review.app==appname).statement,create_engine('sqlite:///db.sqlite3'))
    # print(rdf)
    ctx = {}
    if sentiment=='true':
        senti_data = rdf.analysis.value_counts().reset_index()
        fig =px.pie(senti_data, senti_data['index'], senti_data.analysis,title=f'{appname} sentiment analysis')
        graphJSON1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        ctx['sentiment'] = graphJSON1

    if pol == 'true':
        rdfp = rdf.sort_values('polarity').copy()
        fig =px.area(
        rdfp, 
        'userName', 
        'polarity',
        color='polarity',
        title=f'polarity analysis',
        height=600,
        )
        graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        ctx['polarity'] = graphJSON2

    if subject == 'true':
        rdfs = rdf.sort_values('subjectivity').copy()
        fig =px.histogram(
            rdfs, 
            'subjectivity',
            'userName', 
            color='subjectivity',
            title=f'subjectivity analysis',
            height=600,
        )
        graphJSON3 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        ctx['subjectivity'] = graphJSON3

    db.close()
    return json.dumps(ctx)

@app.route('/about',methods=['GET','POST'])
def about():
    return render_template ('about.html',title='About us')

@app.route('/logout')
def logout():

    session.clear()
    flash('you have been logged out','warning')
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)
