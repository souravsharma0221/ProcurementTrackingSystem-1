import os
from sqlalchemy import create_engine

db_connection_string=os.environ['DB_CONN_STR']
db_connection_string = 'your_connection_string_here'


engine = create_engine(db_connection_string,connect_args={
    "ssl":{
        "ssl_ca":"/etc/ssl/cert.pem"
    }
})

conn=engine.connect()