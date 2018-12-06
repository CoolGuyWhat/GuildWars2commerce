import json
import pandas as pd

#--- Holding Zone ---#
# https://api.guildwars2.com/v2/items?ids=24,68,69,70,71
json1_string ='''
[
  {
    "id": 24,
    "whitelisted": false,
    "buys": {
      "quantity": 53407,
      "unit_price": 162
    },
    "sells": {
      "quantity": 56385,
      "unit_price": 235
    }
  },
  {
    "id": 68,
    "whitelisted": false,
    "buys": {
      "quantity": 1254,
      "unit_price": 61
    },
    "sells": {
      "quantity": 384,
      "unit_price": 129
    }
  },
  {
    "id": 69,
    "whitelisted": false,
    "buys": {
      "quantity": 1682,
      "unit_price": 96
    },
    "sells": {
      "quantity": 709,
      "unit_price": 196
    }
  },
  {
    "id": 70,
    "whitelisted": false,
    "buys": {
      "quantity": 2217,
      "unit_price": 28
    },
    "sells": {
      "quantity": 633,
      "unit_price": 103
    }
  },
  {
    "id": 71,
    "whitelisted": false,
    "buys": {
      "quantity": 641,
      "unit_price": 77
    },
    "sells": {
      "quantity": 1290,
      "unit_price": 114
    }
  }
]
'''
data = json.loads(json1_string)

idict = {}
dlist = []

item_list = []
item_name = ['Sealed Package of Snowballs', 'Mighty Country Coat', 'Mighty Country Coat', 'Mighty Studded Coat', 'Mighty Worn Chain Greaves']

# Puts each entry from Data into the item_list List
for i in range(5):
  item_list.append(data[i])

for i in range(len(item_list)):
  # Sets Variables for each json item in the list
  dict_id = item_list[i]['id']
  dict_name = item_name[i]
  dict_buys_q = item_list[i]['buys']['quantity']
  dict_buys_p = item_list[i]['buys']['unit_price']
  dict_sells_q = item_list[i]['sells']['quantity']
  dict_sells_p = item_list[i]['sells']['unit_price']
  # Creates a list of Dictionaries for Pandas to use
  idict= {}
  idict['id'] = dict_id
  idict['name'] = dict_name
  idict['Buys Quantity'] = dict_buys_q
  idict['Buys Price'] = dict_buys_p
  idict['Sells Quantity'] = dict_sells_q
  idict['Sells Price'] = dict_sells_p
  dlist.append(idict)

panda = pd.DataFrame(dlist)
print(panda)

#for each in item_list:
  # print(type(each)) # Class Dict

#item_list[1]['name'] = item_name[1]
#print(item_list[1])

# Working
#data = json.loads(json1_string)
#print(type(data)) # Class List

#ach_item = []

#Moving down the data list
#for dat in data:
#  for i in range(2):
#    item_list.append(dat[i])

#for i in range(2):
#  print(item_list[i])

### OLD
#Figuring out json dumps 
#dumps_data = json.dumps(data)
#print(type(dumps_data)) # Class String
#print(dumps_data)

#dumps_json_data = json.dumps(json1_string)
#print(type(dumps_json_data)) # Class String
#print(dumps_json_data)

#for dat in data:
#  for da in dat:
#    new_data = da
#print(new_data)
#print(type(new_data)) # Class Dict
