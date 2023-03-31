from database.database import conn
from sqlalchemy import text
import json
import datetime

def addToOrders(userId,productId,timestamp,address,state,city,pincode):
     result=conn.execute(text("insert into orders(user_id,product_id,order_time,address,state,city,pincode) values (:userId,:productId,:timestamp,:address,:state,:city,:pincode)").bindparams(userId=userId,productId=productId,timestamp=timestamp,address=address,state=state,city=city,pincode=pincode))
     order_status_result=conn.execute(text("insert into order_status(order_id,status,expected_delivery) values (:order_id,:status,:date)").bindparams(order_id=result.lastrowid,status="In-Process",date="2022-06-12"))
     product_ids=json.loads(productId)
     for id in product_ids:
          conn.execute(text('update products set quantity=quantity-1 where id=:id').bindparams(id=id))

def getOrders(userId):
     result=conn.execute(text("select * from orders where user_id=:id order by order_time desc").bindparams(id=userId)).all()  
     orders=[]
     for row in result:
          orders.append(dict(row._mapping))
     return orders 
 
def getOrdersForAdmin():
     result=conn.execute(text("select * from orders where id in (select order_id from order_status where status!=:status) order by order_time desc").bindparams(status="Delivered")).all()  
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

def getParticularOrder(order_id):
        result=conn.execute(text("select * from orders where id=:id").bindparams(id=order_id)).fetchone()
        return dict(result._mapping)

def getParticularOrderStatus(order_id):
        result=conn.execute(text("select * from order_status where order_id=:id").bindparams(id=order_id)).fetchone()
        return dict(result._mapping)

def getOrderDetailsForParticularOrder(order):
     ids=json.loads(order['product_id'])
     products=[]
     for id in ids:
          result=conn.execute(text("select * from products where id=:id").bindparams(id=id)).fetchone()
          products.append(dict(result._mapping))     
     return products

def updateOrderStatus(order_id,status):
     if(status=="Delivered"):
           current_date = datetime.date.today().strftime('%Y-%m-%d')
           conn.execute(text('update order_status set status=:status, delivered_on=:date where order_id=:id').bindparams(status=status,id=order_id,date=current_date))
     else:
           conn.execute(text('update order_status set status=:status where order_id=:id').bindparams(status=status,id=order_id))