from flask import Flask, render_template, request
from database.database import getOrders
from models.review_analysis.review import classify
from wtforms import Form, TextAreaField, validators, SelectField
import pickle, joblib
app = Flask(__name__)




class LoginForm(Form):
    phone = TextAreaField('',[validators.DataRequired(),validators.length(10)])
    password = TextAreaField('',[validators.DataRequired(),validators.length(min=8)])
    role = SelectField('',[validators.DataRequired()])

class ReviewForm(Form):
    productreview = TextAreaField('',[validators.DataRequired(),validators.length(min=15)])    

@app.route('/home', methods=['POST', 'GET'])
def home():
    form = LoginForm(request.form)
    if request.method == 'POST':
        return render_template('./admin/index.html')    
 
@app.route('/')
def login():
    # form = LoginForm(request.form)
    # return render_template('login.html')
    form = ReviewForm(request.form)
    return render_template('user/orders.html',form=form)

@app.route('/submitReview',methods=['POST', 'GET'])
def submitReview():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        review = request.form['productreview']
        y, proba = classify(review)
        return render_template('user/_templates/reviewResponse.html',content=review,prediction=y,probability=round(proba*100, 2))
 

 
@app.route('/signup')
def signup():
  return render_template('signup.html') 
   
if __name__ == '__main__':
    app.run()
