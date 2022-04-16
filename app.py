# Взаимодействие с Марусей
# Скилл работает на aiohttp библиотеке, сам скилл - вэб-сервер,
# который отвечает на post-запросы сервера Маруси
import aiohttp
from aiohttp import web
import state
import logic

# Хост и порт, которые прослушивает наш вэб-сервер (Андрей, нужен айпишник и порт)

HOST_IP = "127.0.0.1"
HOST_PORT = 8080


async def health_assistant(request_obj):
    # парсим входной жсон
    request = await request_obj.json()
    print(request)

    # создаём ответ
    response = {}
    response["version"] = request["version"]
    response["session"] = request["session"]
    # закрывать сессию после текущего обращения к скиллу не надо, проставить руками, когда надо будет
    response["response"] = {"end_session": False}
    user_state = state.get_state(request)
    session_state = user_state.get_session_state()
    print(session_state)

    if request["session"]["new"]:
        new_state = logic.get_root_state()
    else:
        current_state = logic.get_state(session_state["current_state_id"])
        print(request["request"]["command"])
        new_state = current_state.get_next_state(request["request"]["command"])

    response["response"]["text"] = new_state.get_text()

    if not new_state.is_end_state():
        session_state["current_state_id"] = new_state.get_id()
        user_state.save_session_state(response)
    else:
        response["response"]["end_session"] = True

    return web.json_response(response)


def init():
    # создание веб-приложения
    app = web.Application()
    # регистрация метода
    app.router.add_post("/health_assistant", health_assistant)
    # запуск
    web.run_app(app, host=HOST_IP, port=HOST_PORT)


if __name__ == "__main__":
    init()