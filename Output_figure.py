
import os
import numpy as np
import matplotlib.pyplot as plt

def mkdir(path):
	folder = os.path.exists(path)
	if  not folder:
		os.makedirs(path)

folder = input('Folder Name: ')
#"QTT_確認期漸增_測試可大於訓練天 _(srand114)美股_DJIA30_訓練65天_NFNT_odd_GNQTS_10000_10_50_0.0004"
dir = "./動態滑動視窗/"
target = dir +  folder
train_Path = target+"/Portfolio/訓練期/"
check_test_Path =  target+"/Portfolio/check_測試期/"
test_Path =  target+"/Portfolio/測試期/"
#QW_Path = "./二次加權導引_(output_testing)/" + sw + "/Portfolio/測試期/"
#Q_Path = "./二次平均導引_(output_testing)/" + sw + "/Portfolio/測試期/"
#Path = "./一次/" + sw + "/Portfolio/測試期/"
all_train_FileList = os.walk(train_Path)
all_check_test_FileList = os.walk(check_test_Path)
all_test_FileList = os.walk(test_Path)
#allQFileList = os.listdir(Q_Path)
#allQWFileList = os.listdir(QW_Path)
#allFileList = os.listdir(Path)

file_name = []
output_train_dir = target + "/output_train/"
output_test_dir = target + "/output_test/"
output_check_test_dir = target + "/output_check_test/"
mkdir(output_train_dir)
mkdir(output_test_dir)
mkdir(output_check_test_dir)
#output_file = "./output/"+sw+"_combine_all.csv"
#output_file_comp = dir + "stock_comp.csv"
#output_file_range = "./output/"+sw+"_fig_range.csv"
#fw = open(output_file, 'a')
#fw_comp = open(output_file_comp, 'a')
#fw_range = open(output_file_range, 'a')
#fw.write("天數,二次加權,一次,二次平均\n")
#fw_comp.write("日期,訓練,撐幾天\n")
train_file_name = []
check_test_file_name = []
test_file_name = []
for root, rdir, files in all_train_FileList:
	train_file_name.append(files)

for root, rdir, files in all_check_test_FileList:
	check_test_file_name.append(files)

for root, rdir, files in all_test_FileList:
	test_file_name.append(files)


for name in train_file_name[0]:
	print(name)
	train_Path_file = train_Path + name
	train_f = open(train_Path_file)
	train_flag = False
	train_data = []
	#fw_comp.write(name + ",")
	for lines in train_f.readlines():
		list = lines.split(',')
		if(list[0] == "初始資金"):
			train_init_fund = float(list[1])
		if(list[0] == "預期報酬"):
			train_parameter = float(list[1])
		#if(list[0] == "Stock#"):
		#	for i in list[1:len(list)-1]:
		#		fw_comp.write(i)
		if(train_flag == True):
			train_data.append(list[len(list)-1])
		if(list[0] == "剩餘資金"):
			train_flag = True
	train_day = len(train_data)
	train_x = np.arange(1,train_day+1)
	new_train_data = []
	for i in train_data:
		i = float(i)
		new_train_data.append(i)
	train_y = new_train_data
	train_Y = train_parameter * train_x + train_init_fund
	plt.figure(1, figsize=(11, 6), dpi=200)
	plt.title(name, fontsize = 14)
	plt.xlabel("Day", fontsize = 16)
	plt.ylabel("Funds Standardization", fontsize = 16)
	plt.xlim(1, train_day)
	plt.xticks(fontsize = 10) # 設定坐標軸數字格式
	plt.yticks(fontsize = 10)
	plt.grid(color = 'gray', linestyle = '-', linewidth = 0.5) # 設定格線顏色、種類、寬度
	line = plt.plot(train_x, train_y, color = "#81C0C0", linewidth = 3, label =
	"Training Portfolio")
	Rline = plt.plot(train_x, train_Y, color = "#000079", linestyle = '--',
	linewidth = 3, label = "Linear Regression")
	plt.legend(loc = 'upper left', fontsize = 12)
	plt.savefig(output_train_dir + name[0:len(name)-4] + ".png")
	#plt.show()
	plt.close()


for name in check_test_file_name[0]:
	print(name)
	check_test_Path_file = check_test_Path + name
	check_test_f = open(check_test_Path_file)
	check_test_flag = False
	check_test_data = []
	for lines in check_test_f.readlines():
		list = lines.split(',')
		if(list[0] == "初始資金"):
			check_test_init_fund = float(list[1])
		if(list[0] == "二次趨勢線"):
			check_test_parameter = list[1]
		if(check_test_flag == True):
			check_test_data.append(list[len(list)-1])
		if(list[0] == "剩餘資金"):
			check_test_flag = True
	check_test_day = len(check_test_data)
	check_test_x = np.arange(1,check_test_day+1)
	new_check_test_data = []
	for i in check_test_data:
		i = float(i)
		new_check_test_data.append(i)
	check_test_y = new_check_test_data
	check_test_parameter = check_test_parameter.split('+')
	check_test1_para = check_test_parameter[0].split(' ')
	check_test2_para = check_test_parameter[1].split('x')
	check_test_Y = float(check_test1_para[0]) *check_test_x **2 +	float(check_test2_para[0]) * check_test_x + check_test_init_fund
	plt.figure(1, figsize=(11, 6), dpi=200)
	plt.title(name, fontsize = 14)
	plt.xlabel("Day", fontsize = 16)
	plt.ylabel("Funds Standardization", fontsize = 16)
	plt.xlim(1, check_test_day)
	plt.xticks(fontsize = 10) # 設定坐標軸數字格式
	plt.yticks(fontsize = 10)
	plt.grid(color = 'gray', linestyle = '-', linewidth = 0.5) # 設定格線顏色、種類、寬度
	check_test_line = plt.plot(check_test_x[0:65], check_test_y[0:65], color = '#FFA042', linewidth = 3, label = "Check Test Portfolio")
	check_test_line2 = plt.plot(check_test_x[64:], check_test_y[64:], color = '#81C0C0', linewidth = 3, label = "Testing Period")
	check_test_QRline = plt.plot(check_test_x, check_test_Y, color = '#FF0000', linestyle = '--', linewidth = 3, label = "Quadratic Regression")
	plt.legend(loc = 'upper left', fontsize = 12)
	plt.savefig(output_check_test_dir + name[0:len(name)-4] + ".png")
	plt.close()

for name in test_file_name[0]:
	print(name)
	test_Path_file = test_Path + name
	test_f = open(test_Path_file)
	test_flag = False
	test_data = []
	for lines in test_f.readlines():
		list = lines.split(',')
		if(list[0] == "初始資金"):
			test_init_fund = float(list[1])
		if(list[0] == "二次趨勢線"):
			test_Q_parameter = list[1]
		if(list[0] == "一次預期報酬"):
			test_L_parameter = float(list[1])
		if(test_flag == True):
			test_data.append(list[len(list) - 1])
		if(list[0] == "剩餘資金"):
			test_flag = True
		
	test_day = len(test_data)
	if (test_day == 1): continue
	test_x = np.arange(1,test_day + 1)
	new_test_data = []
	for i in test_data:
		i = float(i)
		new_test_data.append(i)
	test_y = new_test_data
	test_L_Y = test_L_parameter * test_x + test_init_fund
	test_Q_parameter = test_Q_parameter.split('+')
	test_Q1_para = test_Q_parameter[0].split(' ')
	test_Q2_para = test_Q_parameter[1].split('x')
	if(test_day >= 3):
		test_Q_Y = float(test_Q1_para[0]) * test_x ** 2 + float(test_Q2_para[0]) * test_x + test_init_fund
	plt.figure(1, figsize=(11, 6), dpi=200)
	plt.title(name, fontsize = 14)
	plt.xlabel("Day", fontsize = 16)
	plt.ylabel("Funds Standardization", fontsize = 16)
	plt.xlim(1, test_day)
	plt.xticks(fontsize = 10)                                 # 設定坐標軸數字格式
	plt.yticks(fontsize = 10)
	plt.grid(color = 'gray', linestyle = '-', linewidth = 0.5)  # 設定格線顏色、種類、寬度
	test_line = plt.plot(test_x, test_y, color = "#81C0C0", linewidth = 3, label = "Testing Portfolio")
	test_LRline = plt.plot(test_x, test_L_Y, color = "#000079", linestyle = '--', linewidth = 3, label = "Linear Regression")
	if(test_day >= 3):
		test_QRline = plt.plot(test_x, test_Q_Y, color = "#006030", linestyle = '--', linewidth = 3, label = "Quadratic Regression")
	plt.legend(loc = 'upper left', fontsize = 12)
	plt.savefig(output_test_dir + name[0:len(name) - 4] + ".png")
	plt.close()
##fw_comp.close()
