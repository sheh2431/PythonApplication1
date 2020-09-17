
import os
import numpy as np
import matplotlib.pyplot as plt

def mkdir(path):
	folder = os.path.exists(path)
	if  not folder:
		os.makedirs(path)

		#
sliding_window =  [ "Y2Y", "Y2H", "Y2Q", "Y2M", "H2H", "H2Q","H2M", "H#", "Q2Q", "Q2M", "Q#","M2M", "M#"]

for sw in sliding_window:
	print(sw)
	QW_Path = "./二次加權導引_(output_testing)/" + sw + "/Portfolio/測試期/"
	Q_Path = "./二次平均導引_(output_testing)/" + sw + "/Portfolio/測試期/"
	Path = "./一次/" + sw + "/Portfolio/測試期/"

	allQFileList = os.listdir(Q_Path)
	allQWFileList = os.listdir(QW_Path)
	allFileList = os.listdir(Path)

	allList = os.walk(Q_Path)

	file_name = []
	output_dir = "./output_test/" + sw + "/"
	mkdir(output_dir)
	#output_file = "./output/"+sw+"_combine_all.csv"
	output_file_comp = "./output_test/"+sw+"/" +sw+"_stock_comp.csv"
	#output_file_range = "./output/"+sw+"_fig_range.csv"
	#fw = open(output_file, 'a')
	fw_comp = open(output_file_comp, 'a')
	#fw_range = open(output_file_range, 'a')
	#fw.write("天數,二次加權,一次,二次平均\n")
	fw_comp.write("二次加權,一次,二次平均\n")
	day_init = 3
	for root, dir, files in allList:
		file_name.append(files)
	
	for name in file_name[0]:
		QW_Path_file = QW_Path + name
		Q_Path_file = Q_Path + name
		Path_file = Path + name
		print(name)
	
		QW_f = open(QW_Path_file)
		f = open(Path_file)
		Q_f = open(Q_Path_file)
		QW_flag = False
		Q_flag = False
		flag = False
		QW_data = []
		Q_data = []
		data = []


		fw_comp.write(name + "\n")
	#	fw_range.write(name + "\n")
		for lines in QW_f.readlines():
			list = lines.split(',')
			if(list[0] == "初始資金"):
				QW_init_fund = float(list[1])
			if(list[0] == "Stock#"):
				for i in list[1:len(list)-1]:
					fw_comp.write(i)
			if(list[0] == "二次趨勢線"):
				QW_parameter = list[1]
			if(list[0] == "FS( 1 )"):
				QW_flag = True
			if(QW_flag == True):
				QW_data.append(list[len(list)-1]);


		for lines in f.readlines():
			list = lines.split(',')
			if(list[0] == "初始資金"):
				init_fund = float(list[1])
			if(list[0] == "Stock#"):
				fw_comp.write(",")
				for i in list[1:len(list)-1]:
					fw_comp.write(i)

			if(list[0] == "預期報酬"):
				parameter = float(list[1])
			if(list[0] == "FS( 1 )"):
				flag = True
			if(flag == True):
				data.append(list[len(list)-1]);
		
		for lines in Q_f.readlines():
			list = lines.split(',')
			if(list[0] == "初始資金"):
				Q_init_fund = float(list[1])
			if(list[0] == "Stock#"):
				fw_comp.write(",")
				for i in list[1:len(list)-1]:
					fw_comp.write(i)
				fw_comp.write("\n")
			if(list[0] == "二次趨勢線"):
				Q_parameter = list[1]
			if(list[0] == "FS( 1 )"):
				Q_flag = True
			if(Q_flag == True):
				Q_data.append(list[len(list)-1]);

		c = 1
		day = len(Q_data)
		#print(day)
		#fw.write(name + "," + str(day) + "\n")
		s = day_init
		e = s+day-1
		day_init = e+2
	
		#fw_range.write("'y2y_combine_all'!$b$"+str(s) +":$d$" + str(e) +"\n")
		for i, j, k in zip(QW_data, data, Q_data):
			w_data = "day " + str(c) +","+ i[0:len(i)-1] + "," + j[0:len(j)-1] + "," + k;
			#fw.write(w_data)
			c = c+1
		x = np.arange(1,day+1)
		QW_x = x
		Q_x = x
		new_data = []
		new_QW_data = []
		new_Q_data = []
		for i, j, k in zip(QW_data, data, Q_data):
			i = float(i)
			j = float(j)
			k = float(k)
			new_QW_data.append(i)
			new_data.append(j)
			new_Q_data.append(k)
		y = new_data
		QW_y = new_QW_data
		Q_y = new_Q_data
		#趨勢線
		Y = parameter * x + init_fund
		Q_parameter = Q_parameter.split('+')
		Q1_para = Q_parameter[0].split(' ')
		Q2_para = Q_parameter[1].split('x')
		Q_Y = float(Q1_para[0]) * x **2 + float(Q2_para[0]) * x + Q_init_fund
		QW_parameter = QW_parameter.split('+')
		QW1_para = QW_parameter[0].split(' ')
		QW2_para = QW_parameter[1].split('x')
		QW_Y = float(QW1_para[0]) * x **2 + float(QW2_para[0]) * x + QW_init_fund
	
		plt.figure(figsize=(11, 6), dpi=200)
		plt.title(sw + '_'+ name, fontsize = 14)
		plt.xlabel("Day", fontsize = 16)
		plt.ylabel("Funds Standardization", fontsize = 16)
		plt.xlim(1, day)
		plt.xticks(fontsize = 10)                                 # 設定坐標軸數字格式
		plt.yticks(fontsize = 10)
		plt.grid(color = 'gray', linestyle = '-', linewidth = 0.5)  # 設定格線顏色、種類、寬度
		line = plt.plot(x, y, color = "#81C0C0", linewidth = 3, label = "Linear Portfolio")
		Rline = plt.plot(x, Y, color = "#000079", linestyle = '--', linewidth = 3, label = "Linear Regression")
		Q_line = plt.plot(Q_x,Q_y, color = '#1AFD9C',  linewidth = 3, label = "Quadratic Average Portfolio")
		QARline = plt.plot(x, Q_Y, color = '#006030', linestyle = '--', linewidth = 3, label = "Quadratic Average Regression")
		QW_line = plt.plot(QW_x,QW_y, color = '#FF9D6F',  linewidth = 3, label = "Quadratic Weighted Portfolio")
		QWRline = plt.plot(x, QW_Y, color = 'red', linestyle = '--', linewidth = 3, label = "Quadratic Weighted Regression")
		#plt.plot(x,y)
		#plt.plot(Q_x,Q_y)
		#plt.plot(QW_x,QW_y)

		plt.legend(loc = 'upper left', fontsize = 12)

		plt.savefig("./output_test/" + sw + "/" + sw + "_comp_" + name[0:len(name)-4] + ".png")
		#plt.clf()
		plt.close()
		#plt.show()
	#	f.close()
	#	f2.close()
	#	f3.close()
	#fw.close()
	#fw_range.close()
	fw_comp.close()


