from database.database import conn
from sqlalchemy import text
import json
from datetime import datetime

def addToOrders(userId,productId,timestamp,address,state,city,pincode):
     result=conn.execute(text("insert into orders(user_id,product_id,order_time,address,state,city,pincode) values (:userId,:productId,:timestamp,:address,:state,:city,:pincode)").bindparams(userId=userId,productId=productId,timestamp=timestamp,address=address,state=state,city=city,pincode=pincode))
     order_status_result=conn.execute(text("insert into order_status(order_id,status,expected_delivery) values (:order_id,:status,:date)").bindparams(order_id=result.lastrowid,status="In-Process",date="2022-06-12"))

def getOrders(userId):
     result=conn.execute(text("select * from orders where user_id=:id order by order_time desc").bindparams(id=userId)).all()  
     orders=[]
     for row in result:
          orders.append(dict(row._mapping))
     return orders  

def getOrderDetails(orders):
     final_list={}
     for order in orders:
          products=json.loads(order['product_id'])
          temp_list=[]
          for id in products:
               result=conn.execute(text("select * from products where id=:id").bindparams(id=id)).fetchone()
               temp_dict=dict(result._mapping)
               temp_dict['order_id']=order['id']
               temp_list.append(temp_dict)      
          final_list[order['order_time']]=temp_list
     return final_list  

def getOrderId(orderTime,userId):
          result=conn.execute(text("select id from orders where user_id=:id and order_time=:orderTime").bindparams(id=userId,orderTime=orderTime)).fetchone()
          return int(result[0])

def getOrderStatus(orders):
     status=[]
     for order in orders:
          result=conn.execute(text("select * from order_status where order_id=:id").bindparams(id=order['id'])).all()  
          for row in result:
           status.append(dict(row._mapping))
     return status
          