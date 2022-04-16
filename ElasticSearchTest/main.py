from elasticsearch import Elasticsearch

### Initialization ###
es = Elasticsearch(
    ["https://username:password@localhost:9200"],
    verify_certs=True
)
Elasticsearch.options(es, ignore_status=[400, 404])


### Create indices ###
result = es.indices.create(index="test_index")
print(result)


### Delete indices ###
result = es.indices.delete(index="test_index")
print(result)


### Insert data ###
es.indices.create(index="test_index")
data = {
    'title': 'TEST TITLE',
    'url': 'http://example.com'
}
result = es.create(index="test_index", id='1', document=data)
print(result)


### Update data ###
data = {
    'title': 'TEST TITLE',
    'url': 'http://example.com',
    'date': '2022-01-01'
}
result = es.update(index="test_index", id='1', doc=data)
print(result)


### Delete data ###
result = es.delete(index="test_index", id='1')
print(result)


### Enquiry data ###
'''
Before we start, install this:
PS> elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v8.1.2/elasticsearch-analysis-ik-8.1.2.zip
'''

es.indices.delete(index="test_index")
es.indices.create(index="test_index")

# insert some data...
datas = [{
    'title': 'TITLE1',
    'url': 'http://example.com/1'
},
    {
    'title': 'TITLE2',
    'url': 'http://example.com/2'
},
    {
    'title': 'TITLE3',
    'url': 'http://example.com/3'
},
]
for data in datas:
    es.index(index="test_index", document=data)

# search...
dsl = {
    'query': {
        'match': {
            'title': 'TITLE1'
        }
    }
}
result = es.search(index="test_index", query=dsl)
print(result)
