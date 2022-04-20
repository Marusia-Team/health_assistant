import aiohttp
from aiohttp import web
import json


#Хост и порт, которые прослушивает наш вэб-сервер (Андрей, нужен айпишник и порт)
HOST_IP = "25.75.59.205"
HOST_PORT = 8080
path = "D:/Study/Diplom stuff/skill/health_assistant/server/test.json"

with open(path) as json_file:
    json_obj = json.load(json_file)
    json_obj2 = json.dumps(json_obj)
print(type(json_obj2))
#async def health_assistant(request_obj):
    # парсим входной жсон
    #print(request_obj)
    #request = await request_obj.json()

    #print(request)
def parse_req(request_obj):
    request = request_obj.json()
    return request



#def init():
    #print("Создание сервера")
    # создание веб-приложения
    #app = web.Application()
    # регистрация метода
    #print("регистрация метода")
    #app.router.add_post("/health_assistant", health_assistant)
    # запуск
    #print("Старт сервера")
    #web.run_app(app, host=HOST_IP, port=HOST_PORT)

if __name__ == "__main__":
    #init()
    parse_req(json_file)