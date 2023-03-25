from flask import Flask, render_template, request, redirect, session,flash,jsonify
from database.database import getOrders
from database.cart import getAllCartItems,getProductDetailsCart,addToCart,removeFromCart,getSubtotalForCart
from database.favourites import getAllFavourites,addToFavourites,removeFromFavourites,getProductDetailsInFavourites
from database.products import getAllProducts,getParticularProduct
from models.review_analysis.review import classify
from wtforms import Form, TextAreaField, validators, SelectField
import pickle, joblib,time,random,os
from database.loginSignup import verify_credentials,addUser,getUserId,getProfile
app = Flask(__name__)

# class ReviewForm(Form):
#     productreview = TextAreaField('',[validators.DataRequired(),validators.length(min=15)])   


def checkLogin():
    if 'user_id' in session:
        return True
    else:
        return False
 
@app.route('/')
def index():
    return redirect('/login')
    # form = ReviewForm(request.form)
    # return render_template('user/orders.html',form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        phone = request.form.get('phone')
        password = request.form.get('password')     
        role = request.form.get('role')     
        if(verify_credentials(phone,password,role)):
            userId=getUserId(phone,role)
            session['user_id']=userId
            if role == 'Admin':
                return redirect('admin/home')
            
            else:
                return redirect('user/home')
        else:
                flash("Incorrent credentials") 
    return render_template("login.html")    



# @app.route('/submitReview',methods=['POST', 'GET'])
# def submitReview():
#     form = ReviewForm(request.form)
#     if request.method == 'POST' and form.validate():
#         review = request.form['productreview']
#         y, proba = classify(review)
#         return render_template('user/_templates/reviewResponse.html',content=review,prediction=y,probability=round(proba*100, 2))

@app.route('/api/favourites/update',methods=['POST','GET'])
def update_favourites():
    if request.method == 'POST':
     if 'favourites_add_submit' in request.form:
        addToFavourites(session['user_id'],request.form.get('product_id'))
     elif 'favourites_remove_submit' in request.form:
        removeFromFavourites(session['user_id'],request.form.get('product_id'))  
    return redirect(request.headers.get('Referer')) 
   
@app.route('/api/cart/update',methods=['POST','GET'])
def update_cart():
    if request.method == 'POST':
     if 'cart_add_submit' in request.form:
        addToCart(session['user_id'],request.form.get('product_id'))
     elif 'cart_remove_submit' in request.form:
        removeFromCart(session['user_id'],request.form.get('product_id'))  
    return redirect(request.headers.get('Referer'))    

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
  if checkLogin():
    return render_template('admin/index.html')
  else:
    return redirect('/login')  
 
@app.route('/user/home')
def user_home():
  if checkLogin():
    cart=getAllCartItems(session['user_id'])
    allProducts = getAllProducts()
    topsale=allProducts.copy()
    random.shuffle(topsale)
    favourites=getAllFavourites(session['user_id'])
    return render_template('user/index.html',allProducts=allProducts,topsale=topsale,favourites=favourites,cart=cart) 
  else:
    return redirect('/login')
  
@app.route('/user/favourites')
def user_favourites():
  if checkLogin():
    cart=getAllCartItems(session['user_id'])
    favourites=getAllFavourites(session['user_id'])
    products=getProductDetailsInFavourites(favourites)
    return render_template('user/favourites.html',products=products,favourites=favourites,cart=cart) 
  else:
    return redirect('/login')  
  
@app.route('/user/orders')
def user_orders():
  if checkLogin():
    cart=getAllCartItems(session['user_id'])
    return render_template('user/favourites.html',cart=cart) 
  else:
    return redirect('/login')  
  
@app.route('/user/profile')
def user_profile():
  if checkLogin():
    cart=getAllCartItems(session['user_id'])
    profile=getProfile(session['user_id'])
    return render_template('user/profile.html',profile=profile,cart=cart) 
  else:
    return redirect('/login') 
   
@app.route('/user/cart')
def user_cart():
  if checkLogin():
    favourites=getAllFavourites(session['user_id'])
    cart=getAllCartItems(session['user_id'])
    cartProducts=getProductDetailsCart(cart)
    subTotal=getSubtotalForCart(cart)
    topsale = getAllProducts()
    return render_template('user/cart.html',cartProducts=cartProducts,topsale=topsale,favourites=favourites,subTotal=subTotal,cart=cart) 
  else:
    return redirect('/login') 

@app.route('/user/product/description/<product_id>')
def user_product_details(product_id):
  if checkLogin():
    favourites=getAllFavourites(session['user_id'])
    cart=getAllCartItems(session['user_id'])
    product=getParticularProduct(product_id)
    topsale = getAllProducts()
    return render_template('user/productDetails.html',topsale=topsale,favourites=favourites,cart=cart,product=product) 
  else:
    return redirect('/login')    
   
if __name__ == '__main__':
    app.config['SECRET_KEY']= '#123miAhhndDSsasjfb&&^&(hjncjbjfoas54656+546'
#     app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
