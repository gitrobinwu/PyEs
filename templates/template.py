#-*- coding:utf-8 -*-
from elasticsearch import Elasticsearch
from datetime import datetime 
import json
import functools 
import mappings 

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
if es.indices.exists_template(name="template_helloworld"):
	print printjson(es.indices.delete_template(name="template_helloworld"))[1]
if es.indices.exists_template(name="template_helloworld_wjdc"):
	print printjson(es.indices.delete_template(name="template_helloworld_wjdc"))[1]


#print printjson(es.indices.delete_template(name="template_failed_login"))
# create=True,仅当模板不存在时创建，create=False，模板存在时，则进行覆盖
# 新建索引模板
if not es.indices.exists_template(name="template_helloworld"):
	print printjson(es.indices.put_template(name="template_helloworld",body=mappings.body,create=True))[1]
if not es.indices.exists_template(name="template_helloworld_wjdc"):
	print printjson(es.indices.put_template(name="template_helloworld_wjdc",body=mappings.helloworld_wjdc,create=True))[1]

# 查看索引模板
if es.indices.exists_template(name="template_helloworld"):
	print printjson(es.indices.get_template(name="template_helloworld"))[1]
if es.indices.exists_template(name="template_helloworld_wjdc"):
	print printjson(es.indices.get_template(name="template_helloworld_wjdc"))[1]




	  
