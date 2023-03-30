from database.database import conn
from sqlalchemy import text

def submitReview(userId,productId,orderId,review,seller,classification,probability):
    result=conn.execute(text("insert into reviews(user_id,product_id,order_id,seller,review,classification,probability) values (:userId,:productId,:orderId,:seller,:review,:classification,:probability)").bindparams(userId=userId,productId=productId,orderId=orderId,review=review,seller=seller,classification=classification,probability=probability))

def getReviews(userId):
    result=conn.execute(text("select * from reviews where user_id=:id").bindparams(id=userId)).all()  
    reviews=[]
    for row in result:
        reviews.append(dict(row._mapping))
    return reviews

def rateSellers():
    results_reviews=conn.execute(text("SELECT seller, classification, COUNT(*) FROM reviews GROUP BY seller, classification")).all()
    results_sellers=conn.execute(text("SELECT distinct seller FROM products")).all()
    response = {}
    for seller in results_sellers:
        response[seller[0]]={'positive': 0, 'negative': 0, 'percentage_positive_reviews':0.0, 'total_reviews':0, 'weighted_score':0}
    
    for result in results_reviews:
        seller = result[0]
        review = result[1]
        count = result[2]
        if seller in response:
            if review == 'positive':
                response[seller]['positive'] = count
            elif review == 'negative':
                response[seller]['negative'] = count
        else:
            if review == 'positive':
                response[seller] = {'positive': count, 'negative': 0}
            elif review == 'negative':
                response[seller] = {'positive': 0, 'negative': count}

    # Calculate the weighted score for each seller
    C = 100  # adjust the weight given to total number of reviews
    for seller in response:
        total_reviews = response[seller]['positive'] + response[seller]['negative']
        if(total_reviews!=0):
            percentage_positive_reviews = (response[seller]['positive'] / total_reviews) * 100
            response[seller]['percentage_positive_reviews'] = percentage_positive_reviews
            response[seller]['total_reviews'] = total_reviews
            weighted_score = (percentage_positive_reviews * total_reviews) / (total_reviews + C)
            response[seller]['weighted_score'] = weighted_score
            
    # Sort the response in descending order of percentage_positive_reviews
    response = dict(sorted(response.items(), key=lambda item: item[1]['weighted_score'], reverse=True))        
    return response  
