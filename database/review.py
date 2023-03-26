from database.database import conn
from sqlalchemy import text

def submitReview(userId,productId,orderId,review,seller,classification,probability):
    result=conn.execute(text("insert into reviews(user_id,product_id,order_id,seller,review,classification,probability) values (:userId,:productId,:orderId,:review,:seller,:classification,:probability)").bindparams(userId=userId,productId=productId,orderId=orderId,review=review,seller=seller,classification=classification,probability=probability))

def getReviews(userId):
    result=conn.execute(text("select * from reviews where user_id=:id").bindparams(id=userId)).all()  
    reviews=[]
    for row in result:
        reviews.append(dict(row._mapping))
    return reviews
