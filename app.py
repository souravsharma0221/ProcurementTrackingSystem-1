from flask import Flask, render_template, request, redirect, session,flash
from database.database import getOrders
from models.review_analysis.review import classify
from wtforms import Form, TextAreaField, validators, SelectField
import pickle, joblib,time
from database.loginSignup import verify_credentials,addUser
app = Flask(__name__)

class ReviewForm(Form):
    productreview = TextAreaField('',[validators.DataRequired(),validators.length(min=15)])        
 
@app.route('/')
def index():
    return redirect('/login')
    # form = ReviewForm(request.form)
    # return render_template('user/orders.html',form=form)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        phone = request.form.get('phone')
        password = request.form.get('password')     
        role = request.form.get('role')     
        if(verify_credentials(phone,password,role)):
            if role == 'Admin':
                # session['phone'] = phone
                return redirect('admin/home')
            
            else:
                return redirect('user/home')
        else:
                flash("Incorrent credentials") 

        # return "<h1>Wrong username or password</h1>"    #if the username or password does not matches 

    return render_template("login.html")    



@app.route('/submitReview',methods=['POST', 'GET'])
def submitReview():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        review = request.form['productreview']
        y, proba = classify(review)
        return render_template('user/_templates/reviewResponse.html',content=review,prediction=y,probability=round(proba*100, 2))
 

 
@app.route('/signup',methods=['POST', 'GET'])
def signup():
  if(request.method == 'POST'):
       name = request.form.get('name')
       phone = request.form.get('phone')
       email = request.form.get('email')
       age = request.form.get('age')
       city = request.form.get('city')
       pincode = request.form.get('pincode')
       password = request.form.get('password')
       cpassword = request.form.get('cpassword')
       gender = request.form.get('gender')
       role="User"

       if len(phone)!=10:
           flash("Invalid Phone Number")       
       elif password!=cpassword:
           flash("Passwords are not matching")
       else:
           status=addUser(name,phone,password,email,city,role,pincode,age,gender)
           if(status=="success"):  
            flash("Signup successful")
            return redirect("/login")
           else:
               flash(status)

  return render_template('signup.html') 

@app.route('/admin/home')
def admin_home():  
  return render_template('admin/index.html')
 
@app.route('/user/home')
def user_home():
  return render_template('user/index.html') 
   
if __name__ == '__main__':
    app.secret_key = '&mittu000'
    # app.run(debug=True)
