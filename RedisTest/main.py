from redis import StrictRedis

### Initialization ###
redis = StrictRedis(host='localhost', port=6379, db=0, password='password', decode_responses=True)
redis.set('name', 'Chihara')
print(redis.get('name'))


### Methods ###
url = "https://www.runoob.com/w3cnote/python-redis-intro.html"
# For more information, see the url above.
