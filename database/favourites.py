from database.database import conn
from sqlalchemy import text

def addToFavourites(userId,productId):
    result=conn.execute(text("insert into favourites(user_id,product_id) values (:userId,:productId)").bindparams(userId=userId,productId=productId))

def removeFromFavourites(userId,productId):
    result=conn.execute(text("delete from favourites where user_id=:userId and product_id=:productId").bindparams(userId=userId,productId=productId))

def getAllFavourites(userId):
    result=conn.execute(text("select * from favourites where user_id=:userId").bindparams(userId=userId))
    favourites=[]
    for row in result.all():
        favourites.append(dict(row._mapping))
    return favourites               