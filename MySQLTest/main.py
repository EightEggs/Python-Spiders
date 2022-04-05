import pymysql

### connect to and create a database ###
db = pymysql.connect(host='localhost', user='root',
                     password='123456', port=3306)
cur = db.cursor()
cur.execute("SELECT VERSION()")
data = cur.fetchone()
print('MySQL version:', data)
cur.execute("CREATE DATABASE spiders DEFAULT CHARACTER SET utf8mb4")
db.close()


### create a table ###
db = pymysql.connect(host='localhost', user='root',
                     password='123456', port=3306, db='spiders')
cur = db.cursor()
sql = "CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL,\
name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY (id))"
cur.execute(sql)


### insert data ###
data = {
    'id': '20220001',
    'name': 'Chihara',
    'age': 20
}
keys = ','.join(data.keys())
vals = ','.join(['%s']*len(data))
sql = f"INSERT INTO students({keys}) VALUES({vals})"
try:
    if cur.execute(sql, tuple(data.values())):
        db.commit()
        print(f'Execute `{sql}` successful.')
except:
    db.rollback()
    print(f'Execute `{sql}` failed.\nRollback complete.')


## update data ###
data = {
    'id': '20220001',
    'name': 'Chihara',
    'age': 21
}
keys = ','.join(data.keys())
vals = ','.join(['%s']*len(data))
sql = f"INSERT INTO students({keys}) VALUES ({vals}) ON DUPLICATE KEY UPDATE "
upd = ','.join('{key}=%s'.format(key=key) for key in data)
try:
    if cur.execute(sql+upd, tuple(data.values())*2):
        db.commit()
        print(f'Execute `{sql+upd}` successful.')
except:
    db.rollback()
    print(f'Execute `{sql+upd}` failed.\nRollback complete.')


### delete data ###
conditions = 'age>20'
sql = f"DELETE FROM students WHERE {conditions}"
try:
    if cur.execute(sql):
        db.commit()
        print(f'Execute `{sql}` successful')
except:
    db.rollback()
    print(f'Execute `{sql}` failed.\nRollback complete.')


### inquiry data ###
sql = "SELECT * FROM students WHERE age>=20"
try:
    cur.execute(sql)
    print('Count:', cur.rowcount)
    row = cur.fetchone()
    while row:
        print('Row:', row)
        row = cur.fetchone()
except:
    print('Error.')
