from database.database import conn
from sqlalchemy import text
import random

def getAllProducts():
        products=getAllProductsForAdmin()
        random.shuffle(products)         
        return products    
    
def getAllProductsForAdmin():
        result=conn.execute(text("select * from products where quantity>0"))
        products=[]
        for row in result.all():
                products.append(dict(row._mapping))        
        return products        

def getParticularProduct(product_id):
        result=conn.execute(text("select * from products where id=:id").bindparams(id=product_id)).fetchone()
        return dict(result._mapping) 

def getSeller(productId):
        result=conn.execute(text("select seller from products where id=:id").bindparams(id=productId)).fetchone()
        return str(result[0])

def getProductsWithZeroQuantity():
        result=conn.execute(text("select * from products where quantity=0"))
        products=[]
        for row in result.all():
                products.append(dict(row._mapping))        
        return products

def updateProductQuantity(product_id,quantity):
        conn.execute(text('update products set quantity=:quantity where id=:id').bindparams(quantity=quantity,id=product_id))