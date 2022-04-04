import json

### read json file ###
with open('data.json', encoding='utf-8') as file:
    str = file.read()
    data = json.loads(str)
    print(data)


### write json file ###
data = [{
    'name': 'Asakawa Chihara',
    'gender': 'male',
    'birthday': '2001-10-17'
}]

with open('data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(data, indent=2, ensure_ascii=False))
# == json.dump(data, open('data.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
