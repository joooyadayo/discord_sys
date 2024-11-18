import config as ini
import mysql.connector
from mysql.connector import Error

dbcon:mysql.connector

async def reload_dbcon():
  global dbcon
  dbcon = None #初期化
  dbcon = mysql.connector.connect(
    host      = ini.ini.database.db_hostname,  # データベースのホスト名
    database  = ini.ini.database.db_name,  # データベース名
    user      = ini.ini.database.db_username,  # データベースのユーザー名
    password  = ini.ini.database.db_pw  # データベースのパスワード
  )

