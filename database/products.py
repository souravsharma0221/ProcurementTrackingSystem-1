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

def getRequiredProducts(category,gender):
        result=conn.execute(text("select * from products where category=:category and gender=:gender").bindparams(category=category,gender=gender)).all()
        products=[]
        for row in result:
                products.append(dict(row._mapping))
        random.shuffle(products)
        return products