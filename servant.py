from weather import Weather

class Servant():
	#类的构造器方法，保持链接和游标
	def __init__(self):
		self.weather = Weather()

	def scan_global_chat(self):
		#这是传入的内容，简单的说就是，需要建立一个数据结构能够用来标注，我是否回应过上面那个【你好】了
		#建立一个索引
		idx = 0
		#这是一个记录有人call我的index的list
		self.order_idx_array=[]
		#记录是否有回应的idx的list
		self.reaction_idx_array=[]
		#这里是先做了一次全图的扫描来建立全局的知识
		for msg in self.chat_content:
			#什么都不用干idx肯定是要自增的
			name = msg[0]
			msg = msg[1]
			#[('', '嗯'), ('', '你好'), ('', '@柠檬叔你好'), ('myself', '你好你好'), ('', '@柠檬叔你好')]
			#reaction_idx_array=[3]
			if name == "myself":
				self.reaction_idx_array.append(idx)
			call_token = "@柠檬叔"
			#检测是否有关键词出现，就是有人at机器人没有
			if_be_called = call_token in msg
			if if_be_called:
				#[('', '嗯'), ('', '你好'), ('', '@柠檬叔你好'), ('myself', '你好你好'), ('', '@柠檬叔你好')]
				#order_idx_array=[2,4]
				self.order_idx_array.append(idx)
			idx=idx+1


	def had_react(self,cur):
		print("===had_react sub process===")
		print("===order_idx_array===")
		print(self.order_idx_array)
		print("===reaction_idx_array===")
		print(self.reaction_idx_array)
		print("===cur===")
		print(cur)
		action = True
		#当前找到at语句的行的值（这个行号是所有语句的序列行号）
		#[('', '嗯'), ('', '你好'), ('', '@柠檬叔你好'), ('myself', '你好你好'), ('', '@柠檬叔你好')]
		# cur = 2
		# [2,4]
		# ===> 0
		current_order_index_value = cur
		#初始化一个寻找变量
		found_order_idx_value_s_idx = 0
		#初始化一个index
		tem_idx = 0
		#在order_idx_array(所有at语句行号的子空间)里面找当前正在处理的这个at语句的值
		for order_idx in self.order_idx_array:
			#在at语句行号全集里找到了这个东西
			if order_idx == current_order_index_value:
				#如果找到了，那把这个行号所在的集合空间的序号记录下来
				found_order_idx_value_s_idx = tem_idx
				break
			tem_idx =  tem_idx +1

		#然后其实就简单了，上面拿到了一个序号，那么拿着这个序号去reactions的集合里去找同样序号的
		#首先，如果序号不存在，比如，reaction_idx_array[found_order_idx_value_s_idx]
		#					那就说明机器还没回复过这条at命令，那么就把这个判断函数的返回值设定为False
		#如果找到了，那就更简单了:
		#					把返回值设定为True，让外部函数忽略掉这一条at语句即可
		print("==found_order_idx_value_s_idx==")
		print(found_order_idx_value_s_idx)
		print("==len(self.reaction_idx_array)==")
		print(len(self.reaction_idx_array))
		if found_order_idx_value_s_idx> len(self.reaction_idx_array) or found_order_idx_value_s_idx == len(self.reaction_idx_array):
			action = False
		else:
			if self.reaction_idx_array[found_order_idx_value_s_idx]:
				action = True
		print("===action?====")
		print(action)
		return action

	def wait_for_call(self,chat_content):
		reaction = ""
		#[('', '嗯'), ('', '你好'), ('', '@柠檬叔你好'), ('myself', '你好你好'), ('', '@柠檬叔你好')]
		self.chat_content = chat_content
		self.scan_global_chat()

		idx = 0
		for msg in chat_content:
			print(msg)
			#什么都不用干idx肯定是要自增的
			name = msg[0]
			msg = msg[1]
			#[('', '嗯'), ('', '你好'), ('', '@柠檬叔你好'), ('myself', '你好你好'), ('', '@柠檬叔你好')]
			call_token = "@柠檬叔"
			#检测是否有关键词出现，就是有人at机器人没有
			if_be_called = call_token in msg
			if if_be_called:
				print("I am being called with that message")
				print(msg)
				#[('', '嗯'), ('', '你好'), ('', '@柠檬叔你好'), ('myself', '你好你好'), ('', '@柠檬叔你好')]
				#order_idx_array=[2,4]
				had_react = self.had_react(idx)
				print("===had_react??===")
				print(had_react)
				if had_react:
					pass
				else:
					#如果被at了，则提取order出来
					order = msg.replace(call_token,"")
					print("my rev order is :"+order)
					if order == "你好":
						reaction = "你好"
					if order == "未来天气怎么样":
						reaction = self.weather.getWeather()
			else:
				print("no one call me ,ok~~~~")
			idx=idx+1
		return reaction