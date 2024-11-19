import config as ini
import mysql.connector
from mysql.connector import Error


dbcon:mysql.connector


# dbContextをリフレッシュ
async def reload_dbcon():
  global dbcon
  dbcon = None #初期化
  dbcon = mysql.connector.connect(
    host      = ini.ini.database.db_hostname,  # データベースのホスト名
    database  = ini.ini.database.db_name,  # データベース名
    user      = ini.ini.database.db_username,  # データベースのユーザー名
    password  = ini.ini.database.db_pw  # データベースのパスワード
  )

# ユーザーデータのレコードを生成
def create_userdata_record(user_id,user_name):
  reload_dbcon()
  if dbcon.is_connected():
    query = "INSERT INTO tbl_userdata (user_id, user_name, first_react, balance, last_reacted_post_id, posts_count) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor = dbcon.cursor(dictionary=True)
    cursor.execute(query, (user_id,user_name,0,0,0,0))
    dbcon.commit()
    # 作った
    return True
  else:
    # 作れなかった
    return False

# レコードが存在するか確認　存在しなければcreate_userdata_recordへ
def check_userdata_exists(user_id,user_name):
  reload_dbcon()
  if dbcon.is_connected():
    cursor = dbcon.cursor(dictionary=True)
    query = f"SELECT * FROM tbl_userdata WHERE user_id = '{user_id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
      # 存在するので何もしない
      return
    else:
      # 無いのでつくります
      if create_userdata_record(user_id,user_name):
        # 作りました
        return
      else:
        # 作れませんでした
        return
  else:
    # 接続できなかった
    return



# 収入処理
def benefit(user_id,price):
  reload_dbcon()
  if dbcon.is_connected():
    cursor = dbcon.cursor(dictionary=True)
    query = f"SELECT balance FROM tbl_userdata WHERE user_id = '{user_id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
      balance = result["balance"]
      new_balance = int(balance) + int(price)
      update_query = f"UPDATE tbl_userdata SET balance = {new_balance} WHERE user_id = '{user_id}'"
      cursor.execute(update_query)
      dbcon.commit()
    # 受け取りました
    return True
  else:
    # 何らかの理由で接続できなかった
    return False




# 支払処理
def payment(user_id,price):
  reload_dbcon()
  if dbcon.is_connected():
    cursor = dbcon.cursor(dictionary=True)
    query = f"SELECT balance FROM tbl_userdata WHERE user_id = '{user_id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
      balance = result["balance"]
      new_balance = int(balance) - int(price)
      update_query = f"UPDATE tbl_userdata SET balance = {new_balance} WHERE user_id = '{user_id}'"
      cursor.execute(update_query)
      dbcon.commit()
    # 購入しました
    return True
  else:
    # 何らかの理由で接続できなかった
    return False





# 購入可能か確認
def check_payable(user_id,price):
  reload_dbcon()
  if dbcon.is_connected():
    cursor = dbcon.cursor(dictionary=True)
    query = f"SELECT * FROM tbl_user_data WHERE user_id = '{user_id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
      balance = int(result["balance"])
      pay = int(price)
      if balance >= pay:
        # 買える
        return True
      else:
        # 買えない
        return False
    else:
      # そもそもレコードがない(基本ここには来ない)
      return False





# ロールを購入しようとしているのかを確認
# 戻り値
# True→ロール名,価格
# False→False,False
def get_purchase_role(ch_id,post_id):
  reload_dbcon()
  if dbcon.is_connected():
    cursor = dbcon.cursor(dictionary=True)
    query = f"SELECT * FROM tbl_purchase_role WHERE ch_id = '{ch_id}' AND post_id = '{post_id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
      name = result["role_name"]
      price = result["price"]
      # ロール名と価格をreturn
      return name,price
    else:
      # ロール購入のためのリアクションではないことをreturn
      return False,False
  else:
    # 接続できなかった
    return False, False





def get_channel_rate(ch_id):
  reload_dbcon()
  if dbcon.is_connected():
    cursor = dbcon.cursor(dictionary=True)
    query = f"SELECT * FROM tbl_channel_rate WHERE ch_id = '{ch_id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
      # 特殊レートを返す
      benefit_active = result["benefit_active"]
      benefit_passive = result["benefit_passive"]
      return benefit_active,benefit_passive
    else:
      # 基本レートを返す
      return ini.ini.rate.basic_active,ini.ini.rate.basic_passive
  else:
    return


def check_donation_emoji(emoji_name):
  reload_dbcon()
  if dbcon.is_connected():
    cursor = dbcon.cursor(dictionary=True)
    query = f"SELECT * FROM tbl_donation_emoji WHERE emoji_id = '{emoji_name}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
      price = result["price"]
      return price
    else:
      # 結果なし　贈与絵文字以外
      return False
  else:
    # 接続できなかった
    return False

def check_first_reacted(user_id):
  reload_dbcon()
  if dbcon.is_connected():
    cursor = dbcon.cursor(dictionary=True)
    query = f"SELECT * FROM tbl_user_data WHERE user_id = '{user_id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
      first_react = result["first_react"]
      if first_react == '0':
        # 初回ボーナス未受取
        return False
      elif first_react == '1':
        # 既に初回ボーナス受け取り済み
        return True
    else:
      # 結果なし
      return True
  else:
    # 接続できなかった
    return True

def check_dub_reacting(user_id,post_id):
  reload_dbcon()
  if dbcon.is_connected():
    cursor = dbcon.cursor(dictionary=True)
    query = f"SELECT * FROM tbl_user_data WHERE user_id = '{user_id}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
      last_reacted_post_id = result["last_reacted_post_id"]
      # 今回リアクションと前回リアクションが同じとき
      if last_reacted_post_id == post_id:
        return True
      else:
        return False
    else:
      # 結果なし
      return False
  else:
    # 接続できなかった
    return False

def upd_user_reacted_post(user_id,post_id):

  return
