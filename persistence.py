import sqlite3
import datetime

class Persistence():
	#类的构造器方法，保持链接和游标
	def __init__(self):
		self.con = sqlite3.connect('msgs.db')
		self.cur = self.con.cursor()
		print("Open the database")

	#初始化数据库，只调用一次
	def init_db(self):
	# Create table
	# cur.execute('''CREATE TABLE sync (id text, title text, href text, status int, time timestamp)''')
		self.cur.execute('''CREATE TABLE msgs (id INTEGER PRIMARY KEY, name text, msg text, time timestamp)''')
		return 1

	#保存数据到数据库
	def sav_to_db(self,chat_content):
		sync_counter = 0
		for msg in chat_content:
			print(msg)
			name = msg[0]
			msg = msg[1]
			saved_in_db = self.cur.execute("SELECT * FROM msgs WHERE msg=:msg", {"msg": msg})
			if saved_in_db.fetchall():
			#数据库里查到了条目，暂时不需要去管它是什么状态，直接跳过就好
				pass
			else:
				#数据库里没有这个条目则插入之
				print("I am going to be synced....")
				sync_counter = sync_counter +1
				#https://cloud.tencent.com/developer/article/1997323 
				#自增ID的处理参考
				self.cur.execute("insert into msgs values (NULL,?,?,?)", (name,msg,datetime.datetime.now()))
		#提交所有不在数据库里，需要同步的数据库的记录
		self.con.commit()
		if not sync_counter:
			print("Nothing to be sync....."+ str(datetime.datetime.now()))
		else:
			print("I just sync "+str(sync_counter)+ " rows to database")

	#类的析构器，主要就是关闭数据库链接
	def __del__(self):
		self.cur.close()
		self.con.close()
		print("Close the database")