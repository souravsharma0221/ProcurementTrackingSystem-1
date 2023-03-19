from database.database import conn
from sqlalchemy import text


def verify_credentials(phone,password,role):
    result=conn.execute(text("select * from users where phone = :phone and role = :role").bindparams(phone=phone,role =role)).all()
    if len(result) == 0:
        return False
    else:
        if result[0].password==password:
            return True
        else:
            return False
        
def addUser(name,phone,password,email,city,role,pincode,age,gender):
    result=conn.execute(text("insert into users(name,password,role,phone,email,gender,age,city,pincode) values (:name,:password,:role,:phone,:email,:gender,:age,:city,:pincode)").bindparams(name=name,password=password,role=role,phone=phone,email=email,gender=gender,age=age,city=city,pincode=pincode))

