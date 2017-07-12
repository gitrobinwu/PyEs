#-*- coding:utf-8 
from elasticsearch import Elasticsearch 
import json
import functools 

user = 'admin'
password = 'robinwu2017'
host = '127.0.0.1:9200'

# decorator 
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

# es client 	
es = Elasticsearch(
		['http://%s:%s@%s' % (user,password,host)],
		verify_certs=False 
		)
print printjson(es.info())
print es.ping() 

# analyzer  
print printjson(es.indices.analyze(analyzer="standard",text="hello world"))


## get_template 
# name – The name of the template 
print printjson(es.indices.get_template(name="logstash"))

##### 

# global 
#1. ignore 
#2. timeout connection_timeout request_timeout 
#3. response filtering 
# eg: es.search(index='test-inedx',filter_path=['hits.hits._id','hits.hits._type'])

#######################################################
# exists --> es.indices.exists 
# put_template --> es.indices.put_template  
# get_template --> es.indices.get_template 
# create --> es.indices.create 

###### Document API ############ 
# bulk ---> es.client 

# create --> es.create 
# index --> es.create 

# get --> es.get 
# get_source --> es.get_source 
# mget --> es.mget 
# count --> es.count 
# search --> es.search --> dsl or q 

# update --> es.update 
# delete --> es.delete 

# reindex --> es.reindex 
#########################################################
######### Indices API ######### 
# close --> es.indices.close(index='test-index')
# open --> es.indices.open

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


# cluster mananger 
print '#'*30+"Cluster"+'#'*30 
print printjson(es.cluster.health())
#print printjson(es.cluster.stats())

print '#'*30+"Cat"+'#'*30 
print printjson(es.indices.open(index="syslog-ads-2017.07.11"))
print es.cat.indices(index="syslog-ads-*")
#print es.cat.indices(index="ads-log")

#name – A comma-separated list of alias names to return
print es.cat.aliases(name="ads-log")

# Count provides quick access to the document count of the entire cluster, or individual 
# index – A comma-separated list of index names to limit the returned information 
print es.cat.count(index="All-log")

print printjson(es.cat.health(format="json"))
#print es.cat.help() 

# Shows information about currently loaded fielddata on a per-node basis.
#print printjson(es.cat.fielddata(format="json"))

# Displays the master’s node ID, bound IP address, and node name.
#print es.cat.master(format="json")
 
#print printjson(es.cat.nodes(format="json"))
#print printjson(es.cat.plugins(format="json"))
#print printjson(es.cat.segments(format="json"))
#print printjson(es.cat.thread_pool(format="json"))

##### repositories and snapshots ### 
print printjson(es.cat.repositories(format="json"))
#repository – Name of repository from which to fetch the snapshot information
#print printjson(es.cat.snapshots(name="",format="json"))

print '#'*30+"Snapshots"+'#'*30
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
print printjson(es.snapshot.get_repository(repository="my_backup"))
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
print printjson(es.snapshot.get(repository="my_backup",snapshot="snapshot_1"))

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
print '#'*30+"Helpers"+'#'*30
# Bulk helper 
# There are several helpers for the bulk API since it’s requirement for specific formatting and other considerations can make it cumbersome if used directly.

# The bulk() api accepts index, create, delete, and update actions. Use the _op_type field to specify an action (_op_type defaults to index)



