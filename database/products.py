from database.database import conn
from sqlalchemy import text
import random

def getAllProducts():
        result=conn.execute(text("select * from products"))
        products=[]
        for row in result.all():
                products.append(dict(row._mapping))
        random.shuffle(products)         
        return products        

def getParticularProduct(product_id):
        result=conn.execute(text("select * from products where id=:id").bindparams(id=product_id)).fetchone()
        return dict(result._mapping) 

def getSeller(productId):
        result=conn.execute(text("select seller from products where id=:id").bindparams(id=productId)).fetchone()
        return str(result[0])