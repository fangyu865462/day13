import json

with open("C:/Users/34542/Desktop/data.json",'r',encoding='utf-8') as f:
     for read in f:
         data = json.loads(read)
         print(data)
#[ 要取什么   for   每一个元素   in   从哪里取 ]
name_liat = [user['name'] for user in data['users']]
print(name_liat)