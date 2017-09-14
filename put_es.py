#-*- coding:utf-8 -*- 
from get_xlsx import read_xlsx 
from elasticsearch import Elasticsearch
import time 
import json
import functools 

user = 'admin'
password = 'admin'
host = '127.0.0.1:9200'

#------------------ decorator ----------------------
def esjson(func):
	@functools.wraps(func)
	def wrapper(*args,**kw):
		 res = func(*args,**kw)
		 data = json.dumps(res,sort_keys=True,indent=4,separators=(',',':'),encoding='gbk',ensure_ascii=True)
		 return res,data
	return wrapper 

@esjson
def printjson(func):
	return func 

#---------------- es clinet ------------------------
es = Elasticsearch(
		['http://%s:%s@%s' % (user,password,host)],
		verify_cert=False 
		)
#print type(printjson(es.info())[1])
#print es.ping 
#---------------------------------------------------

index = "helloworld-wjdc"
type = "wjdc"
num=0

# 入库到es 
def write_es(filename):
	global num 
	sheets = read_xlsx(filename)
	# time.strftime("%Y-%m-%d",time.localtime())
	for xlsx_data in sheets:
		xlsx_data.pop(0)
		for row in xrange(len(xlsx_data)):
			body = {
				"school": xlsx_data[row][0],
				"academy": xlsx_data[row][1],
				"name": xlsx_data[row][2],
				"sex": xlsx_data[row][3],
				"grade": xlsx_data[row][4],
				"major": xlsx_data[row][5],
				"interested_project": xlsx_data[row][6],
				"phone_number": xlsx_data[row][7]
			}
			num+=1
			if num in xrange(0,10):
				id = "00%d" % (num,)
			elif num in xrange(10,100):
				id = "0%d" % (num,)
			else:
				id = "%d" % (num,)

			print printjson(es.index(index=index,doc_type=type,id=id,op_type='index',body=body))
		

if __name__ == '__main__':
	# 如果索引已经存在，则删除索引
	if es.indices.exists(index=index):
		print printjson(es.indices.delete(index=index))[1]
	path = ["./wj1.xlsx","./wj.xlsx"]
	for file in path:
		write_es(file)		


