import os
from sqlalchemy import create_engine,text

# db_connection_string="mysql+pymysql://97u0ldqmsxcbei5okci8:pscale_pw_LshPuWsTJ9MfLvLO9slx3DrCB9wNW9qtpVrqLt8m726@ap-south.connect.psdb.cloud/pts?charset=utf8mb4"
db_connection_string=os.environ['DB_CONN_STR']

engine = create_engine(db_connection_string,connect_args={
    "ssl":{
        "ssl_ca":"/etc/ssl/cert.pem"
    }
})

conn=engine.connect()

def getOrders():
    result=conn.execute(text("select * from orders"))
    return result.all()