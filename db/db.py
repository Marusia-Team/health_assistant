import psycopg2
import random
from psycopg2 import Error
active_table = {'green':'fitnes_1', 'blue':'fitnes_2'}
def new_connection(connection):
    try:
        #connection = psycopg2.connect(user="postgres",
                                    #password="Olya19042000",
                                    #host="127.0.0.1",
                                    #port="5432",
                                    #database="health_assistant")
        print("Connection", connection)
        cursor = connection.cursor()
        print("Info about server")
        print(connection.get_dsn_parameters(), "\n")
        cursor.execute("Select version();")
        record = cursor.fetchone()
        print("You connected to ", record, "\n")
        print(cursor)
        return cursor
    except (Exception, Error) as error:
        print("Error: ", error)
def insert_into_recipes(connection,cursor, record):
    try:
        insert_query_template = """INSERT INTO recipes (ingridients,cooking_type,recipe,dish_type) VALUES 
                                ({r_ingridients}, {r_cooking_type}, {r_recipe}, {r_dish_type})"""
        insert_query = insert_query_template.format(r_ingridients='\'' + record["ingridients"] + '\'' ,
                                                    r_cooking_type='\'' + record["cooking_type"] + '\'',
                                                    r_recipe='\'' + record["recipe"] + '\'',
                                                    r_dish_type='\'' + record["dish_type"] + '\'' )
        #cursor = connection.cursor()
        print(cursor)
        cursor.execute(insert_query)
        print(cursor)
        connection.commit()
        print(cursor)
        print("1 запись успешно вставлена")
        return cursor
    except (Exception, Error) as error:
        print("Error: ", error)

def insert_into_fitnes(connection, cursor, record):
    try:
        insert_query_template = """INSERT INTO fitnes_1 (body_part,equipment,gif_url,name, target) VALUES
                                ({r_body_part}, {r_equipment}, {r_gif_url}, {r_name},{r_target})"""
        insert_query = insert_query_template.format(r_body_part='\'' + record["bodyPart"] + '\'',
                                                    r_equipment='\'' + record["equipment"] + '\'',
                                                    r_gif_url='\'' + record["gifUrl"] + '\'',
                                                    r_name='\'' + record["name"] + '\'',
                                                    r_target='\'' + record["target"] + '\'')
        print(cursor)
        cursor.execute(insert_query)
        print(cursor)
        connection.commit()
        print(cursor)
        print("1 запись успешно вставлена")
        return cursor
    except (Exception, Error) as error:
        print("Error: ", error)


def select_from_fitnes(connect, cursor, equipment: str, bodyPart: str) -> list:
    try:
        select_query = f"""select * from fitnes_1 where (equipment = '{equipment}') and (body_part = '{bodyPart}')"""
        cursor.execute(select_query)
        result_req = cursor.fetchall()
        result = result_req[random.randint(1, len(result_req))]
        return result
    except (Exception, Error) as error:
        print('Error: ', error)


def select_from_recipes(connect, cursor, dish_type: str) -> list:
    try:
        select_query = f"""select * from recipes where dish_type = '{dish_type}'"""
        cursor.execute(select_query)
        result_req = cursor.fetchall()
        result = result_req[random.randint(1, len(result_req))]
        return result
    except (Exception, Error) as error:
        print('Error: ', error)
