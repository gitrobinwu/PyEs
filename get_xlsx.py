#-*- coding:utf-8 -*- 

import xlrd 
import sys 
import re

def read_xlsx(filename):
	workbook = xlrd.open_workbook(filename)
	sheets = list() 
	for booksheet in workbook.sheets():
		xlsx_data = list()
		school = None 
		college = None
		for row in xrange(booksheet.nrows):
			rdata = list() 
			for col in xrange(booksheet.ncols):
				cel = booksheet.cell(row,col)
				val = cel.value
				if type(val) is float:val = int(val)
				if type(val) is unicode:val = val.encode('utf-8')
				rdata.append(val)			
			# 数据转换								
			if rdata[0]: school = rdata[0]
			if rdata[1]: college = rdata[1]						 
			if not rdata[0]:rdata[0] = school 
			if not rdata[1]:rdata[1] = college						 
			if type(rdata[4]) is str:
				if re.search(r"四",rdata[4]):
					rdata[4] = 4
				elif re.search(r"三",rdata[4]):
					rdata[4] = 3
				elif re.search(r"二",rdata[4]):
					rdata[4] = 2
				elif re.search(r"一",rdata[4]):
					rdata[4] = 1
			if type(rdata[6]) is str:
				if re.search(r"[、`]",rdata[6]):
					rdata[6] = int(re.split(r"[、`]",rdata[6])[0])
					
			if type(rdata[3]) is str:
				if re.search(r"男",rdata[3]):
					rdata[3] = "男"
				elif re.search(r"女",rdata[3]):
					rdata[3] = "女"
			if not rdata[2]:
				rdata[2] = "其他"
			if not rdata[5]:
				rdata[5] = "其他"
			if not rdata[7]:
				rdata[7] = "其他"

			# 过滤出有效数据
			if rdata[3]: xlsx_data.append(rdata)	
		sheets.append(xlsx_data)										 
	return sheets 
									 
if __name__ == '__main__':
	sheets = read_xlsx(sys.argv[1])
	# 获取所有sheet数据	
	for xlsx_data in sheets:
		for row in xrange(len(xlsx_data)):
			#print xlsx_data[row][6],type(xlsx_data[row][6])
			print xlsx_data[row][0],'\t',xlsx_data[row][1],'\t',xlsx_data[row][2],'\t',xlsx_data[row][3],'\t',xlsx_data[row][4],'\t',xlsx_data[row][5],'\t',xlsx_data[row][6],'\t',xlsx_data[row][7]

