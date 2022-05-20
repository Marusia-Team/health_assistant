import csv
import json
import string
import psycopg2
from db import new_connection, insert_into_recipes

connection = psycopg2.connect(user="postgres",
                            password="Olya19042000",
                            host="127.0.0.1",
                            port="5432",
                            database="health_assistant")
cursor = new_connection(connection)
print("Cursor: " + str(cursor))
def list_to_dict(list):
    dict = {'name':'', 'ingridients':'', 'cooking_type':'', 'recipe':'','dish_type':''}
    dict['name'] = list[1].replace(u'\xa0', u' ')
    dict['ingridients'] = list[2].replace(u'\xa0', u' ')
    dict['cooking_type'] = list[3]
    dict['recipe'] = list[4].replace(u'\r\n', u' ').replace(u'Campbell\'s',u'Campbells')\
        .replace(u'Campbell\' s',u'Campbells').replace(u'l\'ancienne',u'lancienne')\
        .replace(u'Frank\'s', u'Franks').replace(u'Daniel\'s',u'Daniels')\
        .replace(u'д\'оранж',u'ди оранж').replace(u'Hershey\'s',u'Hersheys')
    dict['dish_type'] = list[5]
    return dict

def check(unit):
    unit = unit.strip()
    if unit == 'штука':
        return str(" шт ")
    if unit == 'штуки':
        return str(" шт ")
    if unit == 'по вкусу':
        return str(" ")
    return str(" " + unit + " ")

def update_ingridients(ingridients):
    new_ingridients = ""
    ingridients_list = ingridients.replace(u'[', u'').replace(u']', u'').replace(u'},', u'} ,').replace(u'campbell\'s',u'campbells')\
        .replace(u'd\'epices',u'depices').replace(u'daniel\'s',u'daniels').replace(u'frank\'s','franks')\
        .replace(u'д\'оранж',u'ди оранж').replace(u'Campbell\'s',u'Campbells').replace(u'\'\'',u'\"по вкусу\"').replace(u'\'',u'\"')
    ingridients_list = ingridients_list.split(' , ')
    for item in ingridients_list:
        item = item.replace(u"\"\"", u"")
        item = item.replace(u'\\xa0', ' ' )
        res = json.loads(item)
        keys = list(res.keys())
        new_ingridients = new_ingridients + keys[0] + " " + str(res[keys[0]]) + check(res['unit'] + " ")
    return new_ingridients

with open('all_recepies_inter.csv','r',newline='',encoding='utf-8') as recepies_csv:
    reader = csv.reader(recepies_csv,delimiter='\t')
    for row in reader:
        row_dict = list_to_dict(row)
        row_dict['ingridients'] = update_ingridients(row_dict['ingridients'])
        cursor2 = insert_into_recipes(connection,cursor, row_dict)
        print(cursor2)
        cursor = cursor2
print(row_dict)
cursor.execute("SELECT * from recipes")
record = cursor.fetchall()
print("Результат", record)




