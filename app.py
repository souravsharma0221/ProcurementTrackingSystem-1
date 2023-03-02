from flask import Flask, render_template, request
from database.database import getOrders
from wtforms import Form, TextAreaField, validators, SelectField
import pickle
app = Flask(__name__)


class LoginForm(Form):
    phone = TextAreaField('',[validators.DataRequired(),validators.length(10)])
    password = TextAreaField('',[validators.DataRequired(),validators.length(min=8)])
    role = SelectField('',[validators.DataRequired()])

@app.route('/home', methods=['POST', 'GET'])
def home():
    form = LoginForm(request.form)
    if request.method == 'POST':
        return render_template('./admin/index.html')    
 
@app.route('/')
def login():
    form = LoginForm(request.form)
    return render_template('login.html')
 
 
@app.route('/signup')
def signup():
  return render_template('signup.html') 
   
if __name__ == '__main__':
    app.run()
