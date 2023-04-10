from flask import Flask, render_template, request, redirect, session,flash,jsonify
from database.review import submitReview,getReviews,rateSellers
from database.orders import addToOrders,getOrders,getOrderDetails,getOrderId,getOrderStatus,getOrdersForAdmin,getParticularOrder,getParticularOrderStatus,getOrderDetailsForParticularOrder,updateOrderStatus
from database.cart import getAllCartItems,getProductDetailsCart,addToCart,removeFromCart,getSubtotalForCart,emptyCart
from database.favourites import getAllFavourites,addToFavourites,removeFromFavourites,getProductDetailsInFavourites
from database.products import getAllProducts,getParticularProduct,getSeller,getAllProductsForAdmin,getProductsWithZeroQuantity,updateProductQuantity
from database.inventoryOrders import placeOrderForInventory,getInventoryOrders,getInventoryOrderInfo,updateInventoryOrderStatus
from models.review_analysis.review import classifyReview
from models.demandForecasting.forecastDemand import getForecasts
from models.demandForecasting.previousData import getProductIds,getDataFrame
import random,os,json,pandas as pd
from datetime import datetime,timedelta
from database.loginSignup import verify_credentials,addUser,getUserId,getProfile
from database.schedulers import configure_scheduler,send_email

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

configure_scheduler()

def checkLogin():
    if 'user_id' in session:
        return True
    else:
        return False
 
@app.route('/')
def index():
    return redirect('/login')

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
                flash("Incorrect credentials") 
    return render_template("login.html")   

# User Section 

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
    submittedReviews=getReviews(session['user_id'])
    cart=getAllCartItems(session['user_id'])
    orders=getOrders(session['user_id'])
    orderDetails=getOrderDetails(orders)
    orderStatus=getOrderStatus(orders)
    return render_template('user/myOrders.html',cart=cart,orderDetails=orderDetails,submittedReviews=submittedReviews,orderStatus=orderStatus) 
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
        
@app.route('/user/cart/order')
def user_cart_order():
  if checkLogin():
    cart=getAllCartItems(session['user_id'])
    return render_template('user/checkout.html',cart=cart,orderPrice=getSubtotalForCart(cart)) 
  else:
    return redirect('/login')  

@app.route('/user/orderSuccessfull',methods=['GET','POST'])
def user_order_success():
  if checkLogin():
    if(request.method == 'POST'):
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        pincode = request.form.get('pincode')
        cart=getAllCartItems(session['user_id'])
        timestamp=datetime.now()
        addToOrders(session['user_id'],json.dumps(cart),timestamp,address,state,city,pincode)
        emptyCart(session['user_id'])
        cart=getAllCartItems(session['user_id'])
    return render_template('user/orderPlaced.html',cart=cart) 
  else:
    return redirect('/login')   

@app.route('/user/order/review',methods=['POST','GET'])
def write_review():
    if request.method == 'POST':
       orderTimeStr=request.form.get('order_time')
       orderTime = datetime.strptime(orderTimeStr, '%Y-%m-%d %H:%M:%S')
       productId=request.form.get('product_id')
       orderId=getOrderId(orderTime,session['user_id'])
       seller=getSeller(productId)
       return render_template('user/productReview.html',orderId=orderId,productId=productId,seller=seller)
    return redirect(request.headers.get('Referer'))  

@app.route('/user/order/submitReview',methods=['POST', 'GET'])
def submit_review():
    if request.method == 'POST':
        review = request.form['productreview']
        productId=request.form.get('product_id')
        orderId=request.form.get('order_id')
        seller=request.form.get('seller')
        prediction, proba = classifyReview(review)
        probability=round(proba*100, 2)
        submitReview(session['user_id'],productId,orderId,review,seller,prediction,probability)
        return render_template('user/reviewResponse.html') 
    
#  // User Section   

# Admin Section

@app.route('/admin/home')
def admin_home():  
  if checkLogin():
    data_frame=getDataFrame()
    product_ids=getProductIds()
    data = data_frame.astype({col: 'int' for col in data_frame.columns if col != 'year_month'})
    # Format year_month column as "Month in words, YYYY"
    data['year_month'] = pd.to_datetime(data['year_month'], format='%Y-%m').dt.strftime('%B, %Y')  
    # Reverse the order of the rows
    data = data.iloc[::-1]  
    return render_template('admin/index.html',product_ids=product_ids,data=data)
  else:
    return redirect('/login')  
  
@app.route('/admin/products')
def admin_products():  
  if checkLogin():
    products=getAllProductsForAdmin()
    return render_template('admin/products.html',products=products)
  else:
    return redirect('/login') 
   
@app.route('/admin/forecast_sales')
def admin_forecast_sales():  
  if checkLogin():
    # Determine year and month for next month
    current_year_month = datetime.now().strftime('%Y-%m')
    year, month = current_year_month.split('-')
    next_month = datetime(int(year), int(month), 1) + timedelta(days=32)
    next_year_month = next_month.strftime('%B, %Y')
    forecasts=getForecasts()
    return render_template('admin/forecastSales.html',forecasts=forecasts,next_year_month=next_year_month)
  else:
    return redirect('/login') 
  
@app.route('/admin/orders')
def admin_orders():  
  if checkLogin():
    allOrders=getOrdersForAdmin()
    orderStatus=getOrderStatus(allOrders)
    return render_template('admin/orders.html',allOrders=allOrders,orderStatus=orderStatus)
  else:
    return redirect('/login')
   
@app.route('/admin/inventory_orders')
def admin_inventory_orders():  
  if checkLogin():
    allOrders=getInventoryOrders()
    products=getProductsWithZeroQuantity()
    return render_template('admin/inventoryOrders.html',allOrders=allOrders,products=products)
  else:
    return redirect('/login') 
   
@app.route('/admin/best_suppliers')
def admin_best_suppliers():  
  if checkLogin():
    rating=rateSellers()
    return render_template('admin/bestSuppliers.html',rating=rating)
  else:
    return redirect('/login')  
  
@app.route('/admin/profile')
def admin_profile():  
  if checkLogin():
    profile=getProfile(session['user_id'])
    return render_template('admin/profile.html',profile=profile) 
  else:
    return redirect('/login')  
  
@app.route('/admin/product_details/<product_id>')
def admin_product_details(product_id):  
  if checkLogin():
    product=getParticularProduct(product_id)
    return render_template('admin/productDetails.html',product=product) 
  else:
    return redirect('/login') 
   
@app.route('/admin/order_details/<order_id>')
def admin_order_details(order_id):  
  if checkLogin():
    order=getParticularOrder(order_id)
    order_status=getParticularOrderStatus(order_id)
    products=getOrderDetailsForParticularOrder(order)
    return render_template('admin/orderDetails.html',order=order,order_status=order_status,products=products) 
  else:
    return redirect('/login') 
  
@app.route('/admin/add_stock_to_inventory/<order_id>')
def admin_add_stock_to_inventory(order_id):  
  if checkLogin():
    orderInfo=getInventoryOrderInfo(order_id)
    quantity=orderInfo['quantity']
    product_id=orderInfo['product_id']
    updateInventoryOrderStatus(order_id)
    updateProductQuantity(product_id,quantity)
    return redirect('/admin/inventory_orders') 
  else:
    return redirect('/login') 

@app.route('/admin/update_order_status',methods=['GET','POST'])
def update_order_status():
  if checkLogin():
    if(request.method == 'POST'):
        order_id = request.form.get('order_id')
        status = request.form.get('status')
        updateOrderStatus(order_id,status)
    return redirect('/admin/orders') 
  else:
    return redirect('/login')  
  
@app.route('/admin/placeOrder',methods=['GET','POST'])
def admin_place_order():
  if checkLogin():
    if(request.method == 'POST'):
        quantity = request.form.get('quantity')
        product_id = request.form.get('product_id')
        rating=rateSellers()
    return render_template('/admin/placeOrder.html',quantity=quantity,product_id=product_id,rating=rating) 
  else:
    return redirect('/login') 

@app.route('/admin/orderSuccessfull',methods=['GET','POST'])
def admin_order_success():
  if checkLogin():
    if(request.method == 'POST'):
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        supplier = request.form.get('supplier')
        timestamp=datetime.now()
        placeOrderForInventory(product_id,quantity,supplier,timestamp)
    return render_template('admin/orderPlaced.html') 
  else:
    return redirect('/login')   
  
# // Admin Section       
      
if __name__ == '__main__':
    app.run()
