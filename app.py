# Взаимодействие с Марусей
# Скилл работает на aiohttp библиотеке, сам скилл - вэб-сервер,
# который отвечает на post-запросы сервера Маруси
# для запуска http://localhost:8080/health_assistant@60fe0eae-4314-4905-85af-f4c167677dd5
import aiohttp
from aiohttp import web
import aiohttp_cors
import state
import logic


# Хост и порт, которые прослушивает наш вэб-сервер (Андрей, нужен айпишник и порт)
HOST_IP = "127.0.0.1"
HOST_PORT = 8080


async def health_assistant(request_obj):
    # парсим входной жсон
    request = await request_obj.json()

    # создаём ответ
    response = {"version": request["version"], "session": request["session"], "response": {"end_session": False}}
    # закрывать сессию после текущего обращения к скиллу не надо, проставить руками, когда надо будет
    # берём данные пользователя по сессии
    user_state = state.get_state(request)
    session_state = user_state.get_session_state()
    # берём данные пользователя из персистента
    user_persist_state = state.get_persist_state(request)
    persist_state = user_persist_state.get_persist_state()

    # request.get("session", False).get("new", False)
    if request["session"]["new"]:
        if persist_state == {}:
            new_state = logic.get_root_state()
        else:
            new_state = logic.get_leaf_state()
    else:
        current_state = logic.get_state(session_state["current_state_id"])
        new_state = current_state.get_next_state(request["request"]["command"])

    response["response"]["text"] = new_state.get_text()
    response["response"]["tts"] = new_state.get_tts()
    response["response"]["buttons"] = new_state.get_buttons()
    response["response"]["card"] = new_state.get_card()
    response["response"]["commands"] = new_state.get_commands()

    if not new_state.is_end_state():
        session_state["current_state_id"] = new_state.get_id()
        user_state.save_session_state(response)
    else:
        response["response"]["end_session"] = True

    if persist_state == {}:
        persist_state['calories'] = 0
        user_persist_state.save_session_persist_state(response)
    else:
        persist_state['calories'] += new_state.get_calories()
        user_persist_state.save_session_persist_state(response)

    if response["response"]["end_session"]:
        response["response"]["text"] += str(persist_state['calories'])

    return web.json_response(response)


def init():
    # создание веб-приложения
    app = web.Application()
    # для работы с веб-дебагером
    cors = aiohttp_cors.setup(app,defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    resource = cors.add(app.router.add_resource("/health_assistant"))
    # регистрация метода
    app.router.add_route("POST", "/health_assistant", health_assistant)
    for route in app.router.routes():
        cors.add(route)
    # запуск
    web.run_app(app, host=HOST_IP, port=HOST_PORT)


if __name__ == "__main__":
    init()
