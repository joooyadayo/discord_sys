import configparser
import os

# 各セクションクラス
class DataBaseSection:
	def __init__(self,
			db_hostname,
			db_name,
			db_username,
			db_pw):
		self.db_hostname = db_hostname
		self.db_name = db_name
		self.db_username = db_username
		self.db_pw = db_pw

class ServerSection:
	def __init__(self,
			server_id,
			banker_bot_token,
			mother_bot_token,
			museum_manager_bot_toekn,
			daily_task_bot_token,
			weekly_task_bot_toekn,
			bless_bot_toekn,
			curse_bot_token):
		self.server_id = server_id
		self.banker_bot_token = banker_bot_token
		self.mother_bot_token = mother_bot_token
		self.museum_manager_bot_token = museum_manager_bot_toekn
		self.daily_task_bot_token = daily_task_bot_token
		self.weekly_task_bot_token = weekly_task_bot_toekn
		self.bless_bot_token = bless_bot_toekn
		self.curse_bot_token = curse_bot_token

class RateSection:
	def __init__(self,
			basic_active,
			basic_passive):
		self.basic_active = basic_active
		self.basic_passive = basic_passive

class BlessSection:
	def __init__(self,
			price,
			msg_filepath):
		self.price =price
		self.msg_filepath = msg_filepath

class CurseSection:
	def __init__(self,
			price,
			msg_filepath):
		self.price =price
		self.msg_filepath = msg_filepath

class StartChannelSection:
	def __init__(self,
			post_id,
			benefit,
			msg_filepath):
		self.post_id = post_id
		self.benefit = benefit
		self.msg_filepath = msg_filepath

class BankChannelSection:
	def __init__(self,
			balance_check_ch_id):
		self.balance_check_ch_id=balance_check_ch_id

#全セクションを取りまとめるINIクラス
class INI:
	def __init__(self,
			database,
			server,
			rate,
			bless,
			curse,
			stat_channel,
			bank):
		self.database = database
		self.server = server
		self.rate = rate
		self.bless = bless
		self.curse = curse
		self.start_channel = stat_channel
		self.bank = bank

# msg/テキストファイルの中身を返す
def get_msg(filename):
    with open(filename, 'r', encoding='utf-8') as f:  # ファイルを読み取る
        return f.read()

# ini読み取り
def read_ini(filepath):
	# INIファイルを読み込む
	inicon = configparser.ConfigParser()
	with open(filepath, encoding='utf-8') as f:  # ここでUTF-8を指定
		inicon.read_file(f)
	# iniフォルダの一階層上
	my_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(filepath)))
	# msg フォルダのパス
	msg_dir = os.path.join(my_root_dir, 'msg')
	#======================================
	# セクションごとの値読み取り
	db = 'database'
	database = DataBaseSection(
		db_hostname = inicon.get(db, 'db_hostname'),
		db_name     = inicon.get(db, 'db_name'),
		db_username = inicon.get(db, 'db_username'),
		db_pw       = inicon.get(db, 'db_pw')
	)
	sv = 'server'
	server = ServerSection(
		server_id                   = inicon.get(sv, 'server_id'),
		banker_bot_token			= inicon.get(sv, 'banker_bot_token'),
		mother_bot_token            = inicon.get(sv, 'mother_bot_token'),
		museum_manager_bot_toekn    = inicon.get(sv, 'museum_manager_bot_token'),
		daily_task_bot_token        = inicon.get(sv, 'daily_task_bot_token'),
		weekly_task_bot_toekn       = inicon.get(sv, 'weekly_task_bot_toekn'),
		bless_bot_toekn             = inicon.get(sv, 'bless_bot_toekn'),
		curse_bot_token             = inicon.get(sv, 'curse_bot_token')
	)
	rt = 'rate'
	rate = RateSection(
		basic_active    = inicon.get(rt, 'basic_active',),
		basic_passive   = inicon.get(rt, 'basic_passive'),
	)
	bl = 'bless'
	bless = BlessSection(
		price           = inicon.get(bl, 'price'),
		msg_filepath    = get_msg(os.path.join(msg_dir, inicon.get(bl, 'msg_filepath'))),
	)
	cu = 'curse'
	curse = CurseSection(
		price           = inicon.get(cu, 'price'),
		msg_filepath    = get_msg(os.path.join(msg_dir, inicon.get(cu, 'msg_filepath'))),
	)
	st = 'start'
	start = StartChannelSection(
		post_id         = inicon.get(st, 'post_id'),
		benefit         = inicon.get(st, 'benefit'),
		msg_filepath    = get_msg(os.path.join(msg_dir, inicon.get(st, 'msg_filepath'))),
	)
	bn ='bank'
	bank = BankChannelSection(
		balance_check_ch_id=inicon.get(bn,'balance_check_ch_id')
	)
	# 結果をINIクラスに格納して返す
	return INI(
		database=database,
		server=server,
		rate=rate,
		bless=bless,
		curse=curse,
		stat_channel=start,
		bank=bank
	)