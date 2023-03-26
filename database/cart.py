from database.database import conn
from sqlalchemy import text

def addToCart(userId,productId):
    result=conn.execute(text("insert into cart(user_id,product_id) values (:userId,:productId)").bindparams(userId=userId,productId=productId))

def removeFromCart(userId,productId):
    result=conn.execute(text("delete from cart where user_id=:userId and product_id=:productId").bindparams(userId=userId,productId=productId))

def getAllCartItems(userId):
    result=conn.execute(text("select product_id from cart where user_id=:userId").bindparams(userId=userId))
    cart=[]
    for row in result.all():
        cart.append(int(row[0]))
    return cart

def getProductDetailsCart(cart):
    products=[]
    for id in cart:
        result=conn.execute(text("select * from products where id=:id").bindparams(id=id)).fetchone()
        products.append(dict(result._mapping))
    return products 

def getSubtotalForCart(cart):
    subtotal=0
    for id in cart:
        result=conn.execute(text("select price from products where id=:id").bindparams(id=id)).fetchone()
        subtotal+=int(result[0])
    return subtotal

def emptyCart(userId):
    result=conn.execute(text("delete from cart where user_id=:userId").bindparams(userId=userId))