from apscheduler.schedulers.background import BackgroundScheduler
from models.demandForecasting.forecastDemand import getForecasts
from database.database import conn
from sqlalchemy import text
import math,os
import boto3

session = boto3.Session(
    aws_access_key_id=os.environ['ACCESS_ID'],
    aws_secret_access_key=os.environ['ACCESS_SECRET_CODE'],
    region_name='us-east-1'
)

# Create an SES client
ses_client = session.client('ses')

scheduler=BackgroundScheduler()

def set_threshold():
    forecasts=getForecasts()
    for key,value in forecasts.items():
        conn.execute(text('update products set threshold=:value where id=:key').bindparams(key=key,value=math.ceil(value*0.3)))

def find_products_below_threshold():
    results=conn.execute(text('select id from products where quantity<threshold')).all()
    products=[]
    for row in results:
        products.append(int(row[0]))
    if len(row)>0:
        message="Products with following product IDs are below threshold value\n"+', '.join(products)
        send_email(message)    

def configure_scheduler():
    scheduler.add_job(set_threshold,'interval',hours=24)
    scheduler.add_job(find_products_below_threshold,'interval',hours=1)

    scheduler.start()

def send_email(message):
    try:
        response = ses_client.send_email(
            Source='bmohits0203@gmail.com',
            Destination={
                'ToAddresses': ['mittusudan@gmail.com']
            },
            Message={
                'Subject': {
                    'Data': "Action required for inventory"
                },
                'Body': {
                    'Text': {
                        'Data': message
                    }
                }
            }
        )
    except Exception as e:
        pass   

 

