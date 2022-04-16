import pymongo

### connect to the database ###
client = pymongo.MongoClient(host='localhost', port=27017)
# == client = pymongo.MongoClient('mongodb://localhost:27017')


### select the database & collection ###
db = client['test']
co = db['students']


### insert data ###
data = {
    'id': '20220001',
    'name': 'Chihara',
    'gender': 'male',
    'age': 20
}
result = co.insert_one(data)
# result = co.insert_many(data,...)
print(result)  # <pymongo.results.InsertOneResult object>
print(result.inserted_id)  # a unique _id


### inquiry data ###
result = co.find_one({'name': 'Chihara'})
print(result)  # a dict
results = co.find({'age': 20})
print(results)  # <pymongo.cursor.Cursor object>
for result in results:
    print(result)  # dicts


### update data ###
condition = {'name': 'Chihara'}
student = co.find_one(condition)
student['age'] = 21
result = co.update_one(condition, {'$set': student})
print(result.matched_count, result.modified_count)

condition = {'age': {'$gt': 20}}  # age > 20
result = co.update_many(condition, {'$inc': {'age': 1}})
print(result.matched_count, result.modified_count)


### delete data ###
result = co.delete_one({'name': 'Chihara'})
print(result.deleted_count)

result = co.delete_many({'age': {'$lt': 25}})  # age < 25
print(result.deleted_count)


### other methods ###
'''
co.list_indexes()
co.create_index()
co.create_indexes()
co.drop()
co.drop_index()
co.drop_indexes()
co.find_one_and_delete()
co.find_one_and_replace()
co.find_one_and_update()
co.rename()
...
'''
