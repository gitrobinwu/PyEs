#-*- coding:utf-8 -*-

from elasticsearch import Elasticsearch 
user = 'admin'
password = 'admin'
host = '127.0.0.1:9200'

#global options 
#1, ignore 
# 忽略一些异常

#2, timeout 
# timeout 构造一个客户端时超时时间
# request_timeout 请求超时时间

#3, response filtering (响应过滤)
# filter_path ： reduce the response returned by elasticsearch.
# For example to only return _id and _type:
# es.search(index='test-inedx',filter_path=['hits.hits._id','hits.hits._type'])


# 1, 返回elasticsearch客户端
es = Elasticsearch(
		['http://%s:%s@%s' % (user,password,host)],
		verify_certs=False
		)

# 2,创建索引
# 打开索引
print es.indices.open(index="test-index")
es.indices.create(index='test-index',ignore=400)
# 3,bulk api 
actions = [
{"delete":{"_id":'1'}},
{'create':{"_id":"2"}},
{"key2":"2323"},
{"index":{"_id":"3"}},
{"key3":"4423"}
]

# Perform many index/delete operations in a single API call. 
print es.bulk(index="test-index",doc_type="test",body=actions)
#es.indices.delete(index='test-index',ignore=[400,401])

#body Query DSL 
#analyze_wildcard: Specify whether wildcard and prefix queries should be analyzed (default: false)
#analyzer: The analyzer to use for the query string 
#default_operator: The default operator for query string query (AND or OR), default ‘OR’, valid choices are: ‘AND’, ‘OR’
#q – Query in the Lucene query string syntax
# 返回指定查询数量 
dsl = {
	"query": {
		"match_all":{}
	}	
}
# search-count 
print es.count(index='test-index',doc_type='test',analyze_wildcard=True,q="*")

# 删除文档
es.delete(index='test-index',doc_type='test1',id='4')
# create
# 创建文档
print es.create(index='test-index',doc_type='test1',id='4',body={"key4":"4444444"})

# op_type – Explicit operation type, default ‘index’, valid choices are: ‘index’, ‘create’
# es.index(...,op_type=create)

# info
print '-'*60 
# 查看集群健康以及上线状况
print es.info() 
print es.ping() 


print '-'*60 
# reindex(索引重定向) 
body = {
	"source":{
		"index":"test-index"
	},
	"dest":{
		"index":"new-index"
	}
}
#print es.reindex(body=body)

#search
# Execute a search query and get back search hits that match the query. 
body = {
	"query":{
		"match_all":{}
	}
}
print es.search(index="test-index",doc_type = 'test',q="*")

# get 
print "&"*60 
print "\n"
# Get a typed JSON document from the index based on its id.
print es.get(index="test-index",doc_type = "test",id="10")
# Get the source of a document by it’s index, type and id. 
print es.get_source(index="test-index",doc_type = "test",id="10")
# body – Document identifiers; can be either docs (containing full document information) or ids (when index and type is provided in the URL.
# 批量获取
'''		
body = {
	"docs":[
		{"_id":"10"},
		{"_id":"11"},
		{"_id":"12"}
	]
}
'''

body = {
	"ids": ["10","11","12"]
}
print es.mget(index="test-index",doc_type="test",body=body)
print "\n"
print "&"*60 

#update
# 更新文档
'''
body = {
	"doc":{
		"name":"John Doe"
	}
}

body = {
	"script":"_ctx.source.age +=5"
}
es.update(index="test-index",doc_type='test',id="1",body=body)
'''
# 分析器测试
# analyzer 
print '-'*80
# index - The name of the index to scope the operation 
# body - the text on which the analysis should be performed  
# field - Use the analyzer configured for this field (instead of passing the analyzer name)
#print es.indices.analyze(analyzer="standard",text="hello world")

# close索引
print "*"*60 
#print es.indices.close(index="test-index") 
print es.indices.open(index="test-index")

#################################################
# 创建索引
# index - The name of the index 
# body - The configuration for the index(settings and mappings)
print "#"*80
init = {
	"settings":{
		"index":{
			"number_of_shards":5,
			"number_of_replicas":0,
			"refresh_interval": "5s"
		}
	},
	"mappings":{
		"_default_":{
			"dynamic_templates":[
			{
				"string_fields":{
					"mapping":{
						"fielddata":{
							"format":"disabled"
						},
						"index":"analyzed",
						"omit_norms":"true",
						"type":"string",
						"fields":{
							"raw":{
								"ignore_above":256,
								"type":"string",
								"index":"not_analyzed",
								"doc_values":"true"
							}
						}
					},
					"match_mapping_type":"string",
					"match":"*"
				}
			}
				],
			"numeric_detection":"true",
			"dynamic_date_formats": ["yyyy-MM-dd HH:mm","yyyy-MM-dd","yyyy-MM-dd HH:mm:ss"]
		}
	}
}

es.indices.create(index="robin-index",body=init,ignore=[400,401,404]) 
print 'd'*80
## 删除索引
#  – A comma-separated list of indices to delete;  删除逗号分隔索引列表
# use _all or * string to delete all indices 使用_all 或者 * 删除所有的索引
#es.indices.create(index="test",ignore=[400])
#print es.indices.delete(index="test",ignore=[400,401])

# 删除索引别名
# index – A comma-separated list of index names (supports wildcards); use _all for all indices
# name – A comma-separated list of aliases to delete (supports wildcards); use _all to delete all aliases for the specified indices.
#print es.indices.delete_alias(index="test",name="alias1")

# 删除索引模板
# name – The name of the template 
# es.indices.delete_template(name="tempate_1")

# 检查索引是否存在
# index – A comma-separated list of indices to check 
print es.indices.exists(index="test")
print es.indices.exists_alias(index="test",name="alias")

#####################################################
# 返回索引的一些设置settings mappings 
print es.indices.get(index="test-index",flat_settings=True)

#print es.indices.get_field_mapping(index="test-index",doc_type="test",fields="key1")
print "-"*60
# index – A comma-separated list of index names 
# doc_type – A comma-separated list of document types
print es.indices.get_mapping(index="test-index")

print "*"*80
# index – A comma-separated list of index names; use _all or empty string to perform the operation on all indices
# name – The name of the settings that should be included 
import json 
# filter_path 响应对象，返回过滤
res = es.indices.get_settings(index="test",filter_path=['test.settings.index.version'])
# 字典对象转换成json字符串对象
res_str = json.dumps(res,sort_keys=True,indent=4,separators=(',',':'),encoding='gbk',ensure_ascii=True)
print type(res_str)
print res_str 

print '-'* 100
# u'no permissions for indices:admin/template/get' 
# print es.indices.get_template(name="logstash")

##################
# 创建别名
# body – The settings for the alias, such as routing or filter 
filter = {
	"filter":{
		"term":{
			"filed1":"hello" 
		}
	}
}
print es.indices.put_alias(index="test-index",name="alias1",body=filter) 
res = es.search(index="test-index",doc_type="test",q="*")
res_str = json.dumps(res,sort_keys=True,indent=4,separators=(',',':'),encoding='gbk',ensure_ascii=True)
print type(res_str)
print res_str 

# 查看该索引别名
# index – A comma-separated list of index names to filter aliases 
# name – A comma-separated list of alias names to return 
print es.indices.get_alias(index="test-index")
# 查看字段映射
print es.indices.get_field_mapping(index="test-index",doc_type="test",fields="filed1")

##设置mapping 
res = es.indices.get_mapping(index="test-index") 
res_str = json.dumps(res,sort_keys=True,indent=4,separators=(',',':'),encoding='gbk',ensure_ascii=True)
print type(res_str)
print res_str 

# 更新mapping 
# 给已存在的类型添加新的属性
body = {
	"properties":{
		"key5":{
			"type":"string",
			"fielddata":{
				"format":"disabled"
			}
		}
	}
}
print es.indices.put_mapping(index="test-index",doc_type="test1",body=body)

# 添加新的类型
body = {
	"properties":{
		"key6":{"type":"string"}
	}
}
print es.indices.put_mapping(index="test-index",doc_type = "test2", body=body)

res = es.indices.get_mapping(index="test-index") 
res_str = json.dumps(res,sort_keys=True,indent=4,separators=(',',':'),encoding='gbk',ensure_ascii=True)
print type(res_str)
print res_str 

########
# put_settings 
# Change specific index level settings in real time. 
# body – The index settings to be updated 
# index – A comma-separated list of index names; use _all or empty string to perform the operation on all indices 
res = es.indices.get_settings(index="robin-index") 
res_str = json.dumps(res,sort_keys=True,indent=4,separators=(',',':'),encoding='gbk',ensure_ascii=True)
print type(res_str)
print res_str 

# 更新settings 
body = {
	"number_of_replicas":1,
	"refresh_interval":"10s"
}

print es.indices.put_settings(index="robin-index",body=body)

# 添加一个函数装饰器

print "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
import functools 
def esjson(func):
	@functools.wraps(func)
	def wrapper(*args,**kw):
		res = func(*args,**kw)
		data = json.dumps(res,sort_keys=True,indent=4,separators=(',',':'),encoding='gbk',ensure_ascii=True)
		return data 
	return wrapper 	

@esjson	 
def printjson(func):
	return func
# --> printjson = esjson(printjson)

print printjson(es.indices.get_settings(index="robin-index"))


########################
# Create an index template that will automatically be applied to new indices created. 
# 创建索引模板
# name – The name of the template 
# body – The template definition 

'''
body = {
	"template":"syslog*",
	"settings":{
		"number_of_shards":1
	},
	"mappings":{
		"type1":{
			"_source":{
				"enabled":"false"
			},
			"properties":{
				"host_name":{
					"type":"string"
				}
			}
		}
	}
}

print es.indices.put_template(name="syslog",body=body)
'''
#print es.create(index='test-index1',doc_type='test1',id='4',body={"key4":"4444444"})
#print es.indices.get(index='test-index1')

print '---------- stats -----------------'
print printjson(es.indices.stats(index="robin-index"))

print '#########################################'
# 集群管理API 
print printjson(es.cluster.get_settings(flat_settings=True))
print printjson(es.cluster.health())
print '-'*60 
#print printjson(es.cluster.stats())

# cat API 
print "#######################################"
print es.cat.fielddata(format="json") 
print es.cat.master(format="json") 

# 


