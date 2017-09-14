#-*- coding:utf-8 -*-
# 设置xlsx导入模板
body = {
	"order": 0,
	"template": "helloworld-*",
	"settings": {
		"number_of_shards": 5,
		"number_of_replicas":0,
		"refresg_interval": "5s"
	},
	"aliases":{
		"hw-xlsx": {}
	},
	"mappings": {
		"_default_": {
			"_all": {
				"omit_norms": "true",
				"enabled": "true"
			},
			"numeric_detection":"true",
			"dynamic_templates": [
			{
				"string_fields": {
					"mapping": {
						"fielddata": {
							"format": "disabled"
						},
						"index": "analyzed",
						"omit_norms": "true",
						"type": "string",
						"fields": {
							"raw": {
								"ignore_above": 256,
								"index": "not_analyzed",
								"type": "string",
								"doc_values": "true"
							}
						}
					},
					"match_mapping_type": "string",
					"match": "*"
				}	
			},
			{
				"float_fields": {
					"match": "*",
					"match_mapping_type": "float",
					"mapping": {
						"type": "float",
						"doc_values": "true"
					}
				}
			},
			{
				"double_fields": {
					"match": "*",
					"match_mapping_type": "double",
					"mapping": {
						"type": "double",
						"doc_values": "true"
					}
				}
			},
			{
				"date_fields": {
					"match": "*",
					"match_mapping_type": "date",
					"mapping":{
						"type": "date",
						"doc_values": "true"
					}
				}
			},
			{
				"long_fields": {
					"match": "*",
					"match_mapping_type": "long",
					"mapping": {
						"type": "long",
						"doc_values": "true"
					}
				}
			}
			],
			"properties": {
				"@timestamp": {
					"type": "date",
					"doc_values": "true"
				},
				"@version": {
					"index": "not_analyzed",
					"type": "string",
					"doc_values": "true"
				},
				"host": {
					"type": "string",
					"index": "not_analyzed"
				}
			}
		}
	}
}

#问卷调查模板
helloworld_wjdc = {
	"order": 1,
	"template": "helloworld-wjdc",
	"mappings": {
		"wjdc": {
			"properties": {
				"school": {
					"type": "string",
					"analyzer": "ik_max_word",
					"store": "no",
					"ignore_above": 256,
					"fielddata": {
						"format": "disabled"
					},
				},
				"academy": {
					"type": "string",
					"analyzer": "ik_max_word",
					"store": "no",
					"ignore_above": 256,
					"fielddata": {
						"format": "disabled"
					},
				},
				"name": {
					"type": "string",
					"store": "no",
					"index": "not_analyzed",
					"doc_values": "false",
					"null_value": "NULL"
				},
				"sex": {
					"type": "string",
					"store": "no",
					"index": "not_analyzed",
					"doc_values": "true",
					"null_value": "NULL"

				},
				"grade": {
					"type": "integer",
					"store": "no",
					"doc_values": "true",
				},
				"major": {
					"type": "string",
					"store": "no",
					"index": "not_analyzed",
					"doc_values": "true",
					"null_value": "NULL"
				},
				"interested_project": {
					"type": "integer",
					"store": "no",
					"doc_values": "true",
				},
				"phone_number": {
					"type": "string",
					"store": "no",
					"index": "not_analyzed",
					"doc_values": "false",
					"null_value": "NULL"
				}
			}
		}
	}
}




