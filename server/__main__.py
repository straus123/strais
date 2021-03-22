from pathlib import Path
import os
from dotenv import load_dotenv
from .db import DataBase
from .server import StraisServer

env_path = Path('.') / 'server/.env'
load_dotenv(dotenv_path=env_path)
HOST = os.environ["HOST"]
PORT = int(os.environ["PORT"])
db = DataBase()


srv = StraisServer(host=HOST, port=PORT, db=db)
srv.register()
srv.serve()
