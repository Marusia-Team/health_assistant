import json
import time
import psycopg2
import requests
from deep_translator import GoogleTranslator
from db import insert_into_fitnes,new_connection

body_part = {'waist':'Талия', 'upper legs':'Верхние части ног', 'back':'Спина', 'lower legs':'Нижние части ног',
			'chest':'Грудь', 'upper arms':'Верхние части рук', 'cardio':'Кардио','shoulders':'Плечи',
			'lower arms':'Нижние части рук', 'neck':'Шея'}
target_muscle = {'abs':'Пресс', 'quads':'Квадрицепс', 'lats':'Широчайшие мыщцы спины', 'calves':'Икроножные',
			   'pectorals':'Грудные', 'glutes':'Ягодицы', 'hamstrings':'Подколенные мышцы',
 				'adductors':'Приводящие мышцы', 'triceps':'Трицепс', 'cardiovascular system':'Сердечно-сосудистая система',
			   'spine':'позвоночник', 'upper back':'Верхняя ячасть спины',
 				'biceps':'Бицепс', 'delts':'Дельтовидные мышцы', 'forearms':'Предплечья',
			   'traps':'Трапециевидная мышца', 'serratus anterior':'Передняя зубчатая мышца', 'abductors':'Отводящая мышца',
 				'levator scapulae':'Мышцы лопаток'}
equipment = {'body weight':'Собственный вес', 'cable':'Канат', 'leverage machine':'Рычажный тренажер',
			 'assisted':'Помощь партнера', 'medicine ball':'Медицинский мяч',
 			 'stability ball':'Мяч для удержания равновесия', 'band':'Обруч', 'barbell':'Штанга', 'rope':'Верёвка',
			 'dumbbell':'Гантели', 'ez barbell':'Кривая штанга', 'sled machine':'Тренажер для ног',
			 'upper body ergometer':'Велотренажер для рук', 'kettlebell':'Гиря', 'olympic barbell':'Олимпийская штанга',
 			 'weighted':'С утяжелением', 'bosu ball':'Полусфера для удержания равновесия', 'resistance band':'Резинка',
			 'roller':'Ролик', 'skierg machine':'Лыжный тренажер', 'hammer':'Молот', 'smith machine':'Молот кузнеца',
			 'wheel roller':'Ролик', 'stationary bike':'Велотренажер', 'tire':'Шина', 'trap bar':'Гриф шестиугольный',
			 'elliptical machine':'Элипс', 'stepmill machine':'Лесница'}

connection = psycopg2.connect(user="postgres",
                            password="Olya19042000",
                            host="127.0.0.1",
                            port="5432",
                            database="health_assistant")
cursor = new_connection(connection)
print("Cursor: " + str(cursor))

FIT_API_Adress = "https://exercisedb.p.rapidapi.com/exercises"

URL_AUTH = 'https://developers.lingvolive.com/api/v1.1/authenticate'

fit_headers = {
	"X-RapidAPI-Host": "exercisedb.p.rapidapi.com",
	"X-RapidAPI-Key": "b1efb8b8bfmshc46409ef7497309p118c0ejsn29f45c9a48f0"
}

def en_to_rus(text:str) -> str:
	translated = GoogleTranslator(source='auto', target='ru').translate(text)
	return translated
def translate_body_part(text:str) -> str:
	translated = body_part[text]
	return translated
def translate_target_muscle(text:str) -> str:
	translated = target_muscle[text]
	return translated
def translate_equipment_muscle(text:str) -> str:
	translated = equipment[text]
	return translated

#response = requests.request("GET", FIT_API_Adress, headers=fit_headers)
#print(type(response))
#data = response.json()

#with open('data.txt', 'w') as outfile:
   # json.dump(data, outfile)

with open('data.txt') as json_file:
    data = json.load(json_file)

#print(type(data))
#print(len(data))
time_start = time.time()
for post in data:
#	print(post)
	time_iter_start = time.time()
	new_post = {'bodyPart': translate_body_part(post['bodyPart']), 'equipment': translate_equipment_muscle(post['equipment']),
				'gifUrl': post['gifUrl'], 'name': en_to_rus(post['name']), 'target':translate_target_muscle(post['target'])}
	cursor2 = insert_into_fitnes(connection,cursor,new_post)
	cursor = cursor2
	time_iter_end = time.time()
	print(new_post, "\n", 'iter_time: ', time_iter_end-time_iter_start, "\n\n")
time_end = time.time()
print("Needed time to translate ", len(data), "posts is: ", time_end - time_start)


