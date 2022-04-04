import csv

### read csv file ###
with open('data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    print(list(reader))


### write csv file ###
with open('data.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['id', 'name', 'age'])
    writer.writerows([[10001, 'Asakawa', 20],
                      [10002, 'Billy', 7],
                      [10003, 'Colin', 18]])
# ==
    title = ['id', 'name', 'age']
    writer = csv.DictWriter(csvfile, fieldnames=title, delimiter=',')
    writer.writeheader()
    writer.writerows([{'id': 10001, 'name': 'Asakawa', 'age': 20},
                      {'id': 10002, 'name': 'Billy', 'age': 7},
                      {'id': 10003, 'name': 'Colin', 'age': 18}])
