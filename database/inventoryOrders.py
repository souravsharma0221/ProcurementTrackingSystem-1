from database.database import conn
from sqlalchemy import text

def placeOrderForInventory(productId,quantity,supplier,orderTime):
     result=conn.execute(text("insert into inventory_orders(product_id,quantity,supplier,status,order_time) values (:productId,:quantity,:supplier,:status,:orderTime)").bindparams(productId=productId,quantity=quantity,supplier=supplier,orderTime=orderTime,status="In-Buffer"))

def getInventoryOrders():
     result=conn.execute(text("select * from inventory_orders order by order_time desc")).all()  
     orders=[]
     for row in result:
          orders.append(dict(row._mapping))
     return orders  

def getInventoryOrderInfo(order_id):
        result=conn.execute(text("select * from inventory_orders where id=:id").bindparams(id=order_id)).fetchone()
        return dict(result._mapping)  

def updateInventoryOrderStatus(order_id):
        conn.execute(text('update inventory_orders set status=:status where id=:id').bindparams(status="In-Inventory",id=order_id))  