from database.database import conn
from sqlalchemy import text

def addToFavourites(userId,productId):
    result=conn.execute(text("insert into favourites(user_id,product_id) values (:userId,:productId)").bindparams(userId=userId,productId=productId))

def removeFromFavourites(userId,productId):
    result=conn.execute(text("delete from favourites where user_id=:userId and product_id=:productId").bindparams(userId=userId,productId=productId))

def getAllFavourites(userId):
    result=conn.execute(text("select product_id from favourites where user_id=:userId").bindparams(userId=userId))
    favourites=[]
    for row in result.all():
        favourites.append(int(row[0]))
    return favourites

def getProductDetailsInFavourites(favourites):
    products=[]
    for id in favourites:
        result=conn.execute(text("select * from products where id=:id").bindparams(id=id)).fetchone()
        products.append(dict(result._mapping))
    return products       