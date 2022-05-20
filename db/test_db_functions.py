import psycopg2
from db import new_connection, select_from_fitnes, select_from_recipes
connection = psycopg2.connect(user="postgres",
                            password="Olya19042000",
                            host="127.0.0.1",
                            port="5432",
                            database="health_assistant")
cursor = new_connection(connection)
print("Cursor: " + str(cursor))
fitnes_ex = select_from_fitnes(connection, cursor, 'Собственный вес', 'Спина')
print(fitnes_ex)
recipe = select_from_recipes(connection, cursor, 'салат')
print(recipe)