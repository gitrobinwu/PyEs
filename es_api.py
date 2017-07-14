#-*- coding:utf-8 
from elasticsearch import Elasticsearch 
from elasticsearch import helpers 
from datetime import datetime 
import json
import functools 

user = 'admin'
password = 'robinwu2017'
host = '127.0.0.1:9200'

# print u'----------------- decorator ---------------'
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

# print u'----------------- es client --------------' 	
es = Elasticsearch(
		['http://%s:%s@%s' % (user,password,host)],
		verify_certs=False 
		)
#print printjson(es.info())
#print es.ping() 

# print u'---------------- analyzer ----------------'  
#print printjson(es.indices.analyze(analyzer="standard",text="hello world"))


## get_template 
# name – The name of the template 
#print printjson(es.indices.get_template(name="logstash"))

##### 

# print u'---------------- global -------------------' 
#1. ignore 
#2. timeout connection_timeout request_timeout 
#3. response filtering 
# eg: es.search(index='test-inedx',filter_path=['hits.hits._id','hits.hits._type'])

#######################################################
'''print u'如果索引模板已经存在,删除索引模板: template_robin'
if es.indices.exists_template(name="template_robin"):
	print printjson(es.indices.delete_template(name="template_robin"))
'''

# put_template --> es.indices.put_template  
body = {
	"template":"robin-*",
	"settings":{
		"number_of_shards":1,
		"number_of_replicas":0
	},

	"aliases":{
		"robin-alias":{}
	},

	"mappings":{
		"test":{
			"dynamic_templates":[
			{
				"string_fields": {
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
			"dynamic_date_formats": ["yyyy-MM-dd HH:mm","yyyy-MM-dd","yyyy-MM-dd HH:mm:ss"],
			"numeric_detection":"true"
		}
	}
}

print u"新建索引模板: template_robin:"
# create=True,仅当模板不存在时创建，create=False，模板存在时，则进行覆盖
if not es.indices.exists_template(name="template_robin"):
	print printjson(es.indices.put_template(name="template_robin",body=body,create=True))

print u"判断索引模板是否存在:"
print es.indices.exists_template(name="template_robin")  

# get_template --> es.indices.get_template 
print u"查看索引模板: template_robin:"
'''if es.indices.exists_template(name="template_robin"):
	print printjson(es.indices.get_template(name="template_robin"))
'''

#########################################################
print '\n','-'*80 
'''print u'如果索引已经存在, 则删除索引: robin-index'
if es.indices.exists(index="robin-index"):
	print printjson(es.indices.delete(index="robin-index"))	
'''

#print u'打开和关闭索引:'
# close --> es.indices.close(index='test-index')
# open --> es.indices.open

# create --> es.indices.create 
print u'应用索引模板 template_robin, 新建索引: robin-index'
# es.indices.create(index="robin-index",body=init,ignore=[400,401,404])
if not es.indices.exists(index="robin-index"):
	print printjson(es.indices.create(index="robin-index",ignore=[400,401]))

# exists --> es.indices.exists 
print u"判断索引 robin_index 是否存在:"
print printjson(es.indices.exists(index="robin-index"))

if es.indices.exists(index="robin-index"):
	pass 
	# print u"----------------索引别名--------------"
	'''print u'如果索引别名不存在,添加索引别名 test-alias:'
	# test-alias --> {}
	if not es.indices.exists_alias(index="robin-index",name="test-alias"):
		print printjson(es.indices.put_alias(index="robin-index",name="test-alias"))

	print u'查看索引别名 test-alias 是否存在:'
	print es.indices.exists_alias(index="robin-index",name="test-alias")
	
	print u'删除索引别名 robin-alias:'
	if es.indices.exists_alias(index="robin-index",name="test-alias"):
		print printjson(es.indices.delete_alias(index="robin-index",name="test-alias"))		
	'''

	# print u'---------------- settings mappings ------------' 
	#print u'查看索引 aliases settings mappings:'
	#print printjson(es.indices.get(index="robin-index"))
	#print u'查看索引 aliases:'
	#print printjson(es.indices.get_alias(index="robin-index",name="robin-alias"))
	#print u'查看索引 settings:'
	#print printjson(es.indices.get_settings(index="robin-index"))

	#print 'index type [test] exists:'
	#print printjson(es.indices.exists_type(index="robin-index",doc_type="test"))
	#print u'查看索引 mappings:'
	#print printjson(es.indices.get_mapping(index="robin-index",doc_type="test"))
	

	# print u'------------- update settings ------------------'
	'''body = {
		"number_of_replicas": 1,
		"refresh_interval": "10s"
	}

	print printjson(es.indices.put_settings(index="robin-index",body=body))
	'''

	# print u'-------------- update mapping -------------------'
	'''
	print u'添加新的类型 [test1]'
	body = {
		"properties": {
			"field2": {
				"type":"string"
			}
		}
	}
	
	print printjson(es.indices.put_mapping(index="robin-index",doc_type="test1",body=body)) 
	print printjson(es.indices.get_mapping(index="robin-index",doc_type="test1"))
	print u'查看字段映射[test1][field1]:'
	print printjson(es.indices.get_field_mapping(index="robin-index",doc_type="test1",fields="field1"))
	'''
#########################################################
# index: robin-index
#print printjson(es.indices.get_mapping(index="robin-index",doc_type="test"))
print '\n','-'*80 
print u'在索引 robin-index 新建文档,不指定id，则自动生成:'
#print printjson(es.create(index="robin-index",doc_type="test",id="1",body={"key1":"hello test1","timestamp":datetime.now()}))

# op_type – Explicit operation type, default ‘index’, valid choices are: ‘index’, ‘create’
#print printjson(es.index(index="robin-index",doc_type="test",id="2",op_type="create",body={"key1":"hello test2","timestamp":datetime.now()}))

print u"批量索引文档 es.bulk():"
'''actions = [
	{"delete":{"_id":"1"}},
	{"delete":{"_id":"2"}},
	{"index":{"_id":"3"}},
	{"key1":"hello test3","timestamp":datetime.now()},
	{"index":{"_id":"4"}},
	{"key1":"hello test4","timestamp":datetime.now()}
]
print printjson(es.bulk(index="robin-index",doc_type="test",body=actions))
'''
print u"批量索引文档 helpers.bulk():"
# The bulk() api accepts index, create, delete, and update actions. Use the _op_type field to specify an action (_op_type defaults to index)

#print printjson(es.indices.get_mapping(index="robin-index",doc_type="test"))
#print u'根据文档id删除文档:'
#print printjson(es.delete(index="robin-index",doc_type="test",id="2"))
#print u"判断文档是否存在"
#print printjson(es.exists(index="robin-index",doc_type="test",id="2"))
'''
if es.exists(index="robin-index",doc_type="test",id="5"):
	print printjson(es.delete(index="robin-index",doc_type="test",id="5"))
if es.exists(index="robin-index",doc_type="test",id="6"):
	print printjson(es.delete(index="robin-index",doc_type="test",id="6"))
'''

actions = [
{
	"_op_type": "index",
	"_index":"robin-index",
	"_type":"test",
	"_id":"5",
	"_source":{
		"key1":'hello test5',
		"timestamp":datetime.now()
	}
},
{
	"_op_type": "index",
	"_index":"robin-index",
	"_type":"test",
	"_id":"6",
	"_source":{
		"key1":'hello test6',
		"timestamp":datetime.now() 
	}
}
]
# chunk_size – number of docs in one chunk sent to es (default: 500)
#print printjson(helpers.bulk(es,actions=actions))

# print '----------------- streaming_bulk --------------------'
'''
print type(helpers.streaming_bulk(es,actions=actions,chunk_size=500))
result = helpers.streaming_bulk(es,actions=actions,chunk_size=500)
for document in result:
	print printjson(document)
'''

# print '------------------ parallel_bulk ---------------------'
# thread_count – size of the threadpool to use for the bulk requests
# chunk_size – number of docs in one chunk sent to es (default: 500)
'''
print type(helpers.parallel_bulk(es,actions=actions,thread_count=4,chunk_size=500))
result = helpers.parallel_bulk(es,actions=actions,chunk_size=500)
for document in result:
	print printjson(document)
'''

#print printjson(es.search(index="robin-index",doc_type="test",q="*"))

########################################################################
#print u'根据文档id获取文档:'
#_source – True or false to return the _source field or not, or a list of fields to return
#_source_exclude – A list of fields to exclude from the returned _source field
#_source_include – A list of fields to extract and return from the _source field

#print printjson(es.get(index="robin-index",doc_type="test",id="1"))
#print printjson(es.get(index="robin-index",doc_type="test",id="2"))

'''print u'只返回文档数据:'
print printjson(es.get_source(index="robin-index",doc_type="test",id="2"))

print u"批量获取文档:"
body = {
	"docs":[
		{"_id":"1"},
		{"_id":"2"}
	]
}
body = {
	"ids": ["1","2"]
}
print printjson(es.mget(index="robin-index",doc_type="test",body=body))

print u'局部更新文档:'
body = {
	"doc":{
		"key1":5
	}
}
print printjson(es.update(index="robin-index",doc_type="test",id="2",body=body))
'''

# print u'---------------------reindex api ---------------------------------- '
print u'重定向索引 robin-index --> test-index:'
#print printjson(es.indices.delete(index="test-index"))	
# helpers.reindex 
# query – body for the search() api
# target_client – optional, is specified will be used for writing (thus enabling reindex between clusters)
# chunk_size – number of docs in one chunk sent to es (default: 500)
'''
body = {
	"query":{
		"terms":{
			"key1":["test3","test4"]
		}
	}
}
print printjson(helpers.reindex(es,source_index="robin-index",target_index="test-index",chunk_size=500,query=body))
print printjson(es.search(index="test-index",q="*"))
'''

#print u'------------------- 查询文档es.search: -----------------------------'
# es.search 
# size – Number of hits to return (default: 10) 
# from_ – Starting offset (default: 0)
# _source – True or false to return the _source field or not, or a list of fields to return
# _source = True, _source=["key1"]

# _source_exclude – A list of fields to exclude from the returned _source field
# _source_include – A list of fields to extract and return from the _source field
# - sort – A comma-separated list of <field>:<direction> pairs / desc asc 

# q=* 
# analyzer – The analyzer to use for the query string
# default_operator – The default operator for query string query (AND or OR), default ‘OR’, valid choices are: ‘AND’, ‘OR’
'''
body = {
	"query":{
		"match":{
			"key1":"test1"
		}
	}
}
print printjson(es.count(index="robin-index",doc_type="test",body=body))
print printjson(es.search(index="robin-index",doc_type="test",body=body,_source=["key1"],from_="0",size="1"))

print '--------------- elasticsearch.helpers.scan -------------------'
print u"查询文档elasticsearch.heapers.scan:"
# 不支持 from size  
result = helpers.scan(es,query=body,index="robin-index",doc_type="test",_source=["key1"],raise_on_error=True) 
#result = helpers.scan(es,q="key1:test1",index="robin-index",doc_type="test",_source=["key1"]) 
for document in result:
	print printjson(document) 
'''	
#########################################################

###### Document API ############ 
# bulk ---> es.client 
# es.helpers.bulk
# create --> es.create 
# index --> es.create 

# get --> es.get 
# get_source --> es.get_source 
# mget --> es.mget 
# count --> es.count 
# search --> es.search --> dsl or q 
# es.helpers.scan 

# update --> es.update 
# delete --> es.delete 

# reindex --> es.reindex 
# es.helpers.reindex 
#########################################################
######### Indices API ######### 

#### get api #### 
# get -->es.indices.get  (settings and mappings) 
# get_mappings --> es.indices.get_mappings 
# get_field_mapping --> es.indices.get_field_mapping

# put_alias --> es.indices.put_alias 
# get_alias --> es.indices.get_alias 

## update 
# put_mappings --> es.indices.put_mappings 
# put_settings --> es.indices.put_settings 

############# Delete API ###########
# exists --> es.indices.exists 
# delete --> es.indices.delete 

# exists_alias --> es.indices.exists_alias 
# delete_alias --> es.indices.delete_alias 

# index – A comma-separated list of index names; use _all to check the types across all indices
# doc_type – A comma-separated list of document types to check 
# exists_type --> es.indices.exists_type 

# exists_template --> es.indices.exists_template 
# delete_template --> es.indices.delete_template  

# print u'---------------------- cluster mananger -------------------------'
#print '#'*30+"Cluster"+'#'*30 
#print printjson(es.cluster.health())
#print printjson(es.cluster.stats())

# print u'----------------------- cat API ---------------------------------'	
'''print '#'*30+"Cat"+'#'*30 
#print printjson(es.indices.open(index="syslog-ads-2017.07.11"))
print es.cat.indices(index="syslog-ads-*")
#print es.cat.indices(index="ads-log")

#name – A comma-separated list of alias names to return
print es.cat.aliases(name="ads-log")

# Count provides quick access to the document count of the entire cluster, or individual 
# index – A comma-separated list of index names to limit the returned information 
print es.cat.count(index="All-log")

print printjson(es.cat.health(format="json"))
'''

#print es.cat.help() 

# Shows information about currently loaded fielddata on a per-node basis.
#print printjson(es.cat.fielddata(format="json"))

# Displays the master’s node ID, bound IP address, and node name.
#print es.cat.master(format="json")
 
#print printjson(es.cat.nodes(format="json"))
#print printjson(es.cat.plugins(format="json"))
#print printjson(es.cat.segments(format="json"))
#print printjson(es.cat.thread_pool(format="json"))

# print u'------------------ repositories and snapshots --------------------'
#print printjson(es.cat.repositories(format="json"))
#repository – Name of repository from which to fetch the snapshot information
#print printjson(es.cat.snapshots(name="",format="json"))

#print '#'*30+"Snapshots"+'#'*30
# - repository – A repository name
# - body The repository definition
# - verify – Whether to verify the repository after creation
# create_repository -->es.snapshot.create_repository
'''
body = {
	"type":"fs",
	"settings":{
		"location":"/esdata",
		"compress": "true"
	}
}'''
#print printjson(es.snapshot.create_repository(repository="my_backup",body=body,verify=True))
#Return information about registered repositories.
#print printjson(es.snapshot.get_repository(repository="my_backup"))
# Removes a shared file system repository.
#print printjson(es.snapshot.delete_repository(repository="my_backup1"))
		
# - repository – A repository name
# - snapshot – A snapshot name 
# - body – The snapshot definition
# - wait_for_completion : default false 
# create --> es.snapshot.create 
'''body = {
	"indices":"waf-log",
	"ignore_unavailable": "true",
	"include_global_state": "false"

}'''
#print printjson(es.snapshot.create(repository="my_backup",snapshot="snapshot_2",body=body))

# Retrieve information about a snapshot.
#ignore_unavailable – Whether to ignore unavailable snapshots, defaults to false which means a SnapshotMissingException is thrown
# snapshot: _all / * / snapshot_1 
#print printjson(es.snapshot.get(repository="my_backup",snapshot="snapshot_1"))

#print printjson(es.snapshot.delete(repository="my_backup",snapshot="snapshot_2"))

# restore 
# wait_for_completion – Should this request wait until the operation has completed before returning, default False
'''
body = {
	"indices":"syslog-ads-2017.07.11",
	"ignore_unavailable": "true",
	"include_global_state": "false",
}'''
# bao quan xian chu cuo 
#print printjson(es.snapshot.restore(repository="my_backup",snapshot="snapshot_1",body=body))

#print es.cat.indices(index="syslog-ads-*")

#################################################
#print '#'*30+"Helpers"+'#'*30
# Bulk helper 
# There are several helpers for the bulk API since it’s requirement for specific formatting and other considerations can make it cumbersome if used directly.

# The bulk() api accepts index, create, delete, and update actions. Use the _op_type field to specify an action (_op_type defaults to index)


