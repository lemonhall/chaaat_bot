#https://github.com/opencv/opencv-python
#使用OpenCV和Python从图像中提取形状
#https://blog.csdn.net/weixin_26752765/article/details/108132857

#https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html#:~:text=findContours()%20function%2C%20first%20one,the%20contours%20in%20the%20image.
import numpy as np
import cv2 as cv
from paddleocr import PaddleOCR


class ChatBoxParser:
	def getChatContent():
		ocr = PaddleOCR(use_angle_cls=True, lang="ch")
		#全局开关，打开可视化的调试
		visul_debug = False

		im = cv.imread('chat_box.png')
		imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
		#等于说就是，大于36的都给我变成0
		ret, thresh = cv.threshold(imgray, 28, 255, 0)
		#可视化调试开关
		if visul_debug:
			cv.imshow("gray",imgray)
			cv.waitKey(0)
		else:
			pass
		#https://wenku.baidu.com/view/872340374731b90d6c85ec3a87c24028915f8531.html
		#https://blog.csdn.net/wzh111wzh/article/details/79162321
		# image-寻找轮廓的图像；

		# mode-轮廓的检索模式：
		#     cv2.RETR_EXTERNAL表示只检测外轮廓
		#     cv2.RETR_LIST检测的轮廓不建立等级关系
		#     cv2.RETR_CCOMP建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层。
		#     cv2.RETR_TREE建立一个等级树结构的轮廓。

		# method-为轮廓的近似办法：
		#     cv2.CHAIN_APPROX_NONE存储所有的轮廓点，相邻的两个点的像素位置差不超过1，即max（abs（x1-x2），abs（y2-y1））==1
		#     cv2.CHAIN_APPROX_SIMPLE压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，

		# 例如一个矩形轮廓只需4个点来保存轮廓信息
		#     cv2.CHAIN_APPROX_TC89_L1，CV_CHAIN_APPROX_TC89_KCOS使用teh-Chinl chain 近似算法
		# ————————————————
		# 版权声明：本文为CSDN博主「wzh111wzh」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
		# 原文链接：https://blog.csdn.net/wzh111wzh/article/details/79162321
		contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

		#https://blog.csdn.net/Easen_Yu/article/details/89380578
		#绘制为绿色，-1的话就是填充
		what = cv.drawContours(im, contours, -1, (0,255,0), -1)
		#可视化调试开关
		if visul_debug:
			cv.imshow('drawimg',what)
			cv.waitKey(0)
		else:
			pass

		# imgray2 = cv.cvtColor(what, cv.COLOR_BGR2GRAY)
		# cv.imshow("gray2222222==",imgray2)
		# cv.waitKey(0)
		# #等于说就是，大于36的都给我变成0
		# ret2, thresh2 = cv.threshold(imgray2, 24, 255, 0)

		# contours2, hierarchy2 = cv.findContours(thresh2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
		# #绘制为绿色，-1的话就是填充
		# what2 = cv.drawContours(im, contours2, -1, (0,255,0), -1)
		# print(contours2)
		# cv.imshow('what2====',what2)
		# cv.waitKey(0)

		#http://www.learningaboutelectronics.com/Articles/How-to-find-the-largest-or-smallest-object-in-an-image-Python-OpenCV.php
		#然后感觉就可以开始求面积了
		# def get_contour_areas(contours):

		#     all_areas= []

		#     for cnt in contours:
		#         area= cv2.contourArea(cnt)
		#         all_areas.append(area)

		#     return all_areas

		#给所有在3500~4000面积大小的头像上蓝色来定位头像
		avtars = []
		other_contours=[]
		may_dialogues=[]
		#这部分实际上是在定位头像以及对话框
		#头像是使用了面积法去定位的
		#而对话框则使用了扩充图形与原图形的面积比值系数，以及顶点个数两个特征值去筛选
		#同时对话框一开始就排除了头像的正方形
		for cnt in contours:
			area = cv.contourArea(cnt)
			rect = cv.boundingRect(cnt)
			#print(rect)
			rectArea = rect[2] * rect[3]
			#print(rectArea)
			extent = area / rectArea
			hull =cv.convexHull(cnt)
			hullArea = cv.contourArea(hull, False)
			num_of_point = len(cnt)
			if hullArea:
				solidity = area / hullArea
			else:
				solidity = 0
			#print(area)
			if area>3500 and area <4000:
				avtars.append(cnt)
				print("==avtars area==")
			else:
				other_contours.append(cnt)
				if extent > 0.85 and extent < 0.99 and num_of_point>19 and num_of_point<35:
				#if extent > 0.85 and extent < 0.87:
				#if len(cnt) != 20 and extent > 0.9699:
					may_dialogues.append(cnt)
					print(num_of_point)
					print(extent)
					print(solidity)
					print("==dialogues bubbles==")


		im = cv.imread('chat_box.png')
		avtars_img = cv.drawContours(im, avtars, -1, (255,0,0), -1)
		#可视化调试开关
		if visul_debug:
			cv.imshow('avtars_img====',avtars_img)
			cv.waitKey(0)
		else:
			pass

		im = cv.imread('chat_box.png')
		may_dialogues_img = cv.drawContours(im, may_dialogues, -1, (0,0,255), -1)
		#可视化调试开关
		if visul_debug:
			cv.imshow('may_dialogues_img====',may_dialogues_img)
			cv.waitKey(0)
		else:
			pass

		#所有contours的特征值的文档
		#https://docs.opencv.org/4.x/dc/dcf/tutorial_js_contour_features.html
		#https://docs.opencv.org/4.x/da/dc1/tutorial_js_contour_properties.html
		#https://docs.opencv.org/4.x/d5/daa/tutorial_js_contours_begin.html
		#https://docs.opencv.org/4.x/da/d0a/tutorial_js_contours_hierarchy.html

		#然后是飞桨做ocr了
		#https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.5/doc/doc_en/environment_en.md
		#https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.5/doc/doc_en/whl_en.md#42-numpy-array
		#识别cv2的numpy矩阵图像
		#看来得遍历了
		idx=0
		chat_content=[]
		chat_row=()
		may_dialogues = list(reversed(may_dialogues))
		for dialog_cnt in may_dialogues:
			im = cv.imread('chat_box.png')
			x,y,w,h = cv.boundingRect(dialog_cnt)
			#ROI = image[y1:y2, x1:x2]
			#https://stackoverflow.com/questions/9084609/how-to-copy-a-image-region-using-opencv-in-python
			#这是气泡的大小
			roi=im[y:y+h,x:x+w]
			# 	-------------------------------------------
			# |                                         | 
			# |    (x1, y1)                             |
			# |      ------------------------           |
			# |      |                      |           |
			# |      |                      |           | 
			# |      |         ROI          |           |  
			# |      |                      |           |   
			# |      |                      |           |   
			# |      |                      |           |       
			# |      ------------------------           |   
			# |                           (x2, y2)      |    
			# |                                         |             
			# |                                         |             
			# |                                         |             
			# -------------------------------------------
			#试图去获取名字，那么y和气泡的y是类似的，但是还要减小20左右
			print("======The bubble's x and y===========")
			print(x)
			print(y)
			#====================这一部分是在解析对话者的名字====================
			#这里是规避一个y小于0的错误
			name_y1 = y -45
			if name_y1<0:
				name_y1 =0
			roi_name=im[name_y1:y-5,x-20:x+220]
			#事实证明证明，别人说的话，x坐标大概也就是105左右
			name = ""
			if x < 200:
				someOneName = ocr.ocr(roi_name, cls=True)
				for line in someOneName:
					name = line
					#第一个是一个list，第二个实际上是一个tuple
					if len(name)==2:
						name=name[1][0]
					else:
						name="无法解析"
				#可视化调试开关是否打开了？
				if visul_debug:
					cv.imshow('====roi_name '+str(idx),roi_name)
					cv.waitKey(0)
				else:
					pass
			else:
				name = "myself"
			print("someOne's name:")
			print(name)
			#到此解析结束说话者的名字
			#====================这一部分是在解析对话本身====================
			someOneSay = ocr.ocr(roi, cls=True)
			sentence = ""
			for line in someOneSay:
				if len(line)==2:
					line = line[1][0]
					sentence =  sentence + line
			print(sentence)
			#可视化调试是否开启了
			if visul_debug:
				cv.imshow('====roi '+str(idx),roi)
				cv.waitKey(0)
			else:
				pass
			#for dialog_cnt in may_dialogues:
			#这已经是遍历对话框边缘图形的结尾处了，这里其实就可以插入sql了
			idx=idx+1
			chat_row=(name,sentence)
			chat_content.append(chat_row)

			
		cv.destroyAllWindows()
		return chat_content