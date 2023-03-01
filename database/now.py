from database import conn,text


result=conn.execute(text("select * from orders"))
print(result.all())