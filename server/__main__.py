from .db import DataBase
from .server import StraisServer
HOST = '127.0.0.1'
PORT = 65432
db = DataBase()


srv = StraisServer(host=HOST, port=PORT, db=db)
srv.register()
srv.serve()
