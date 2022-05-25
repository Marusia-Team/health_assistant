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
    # Парсим входной жсон
    global flag
    flag = False
    request = await request_obj.json()

    # Создаём ответ
    response = {"version": request["version"], "session": request["session"], "response": {"end_session": False}}
    # Закрывать сессию после текущего обращения к скиллу не надо, проставить руками, когда надо будет
    # Берём данные пользователя по сессии
    if not request.get("session", False).get("user", False):
        not_auth_state = logic.get_state("102")
        response["response"]["text"] = not_auth_state.get_text()
        response["response"]["tts"] = not_auth_state.get_tts()
        response["response"]["end_session"] = True
    else:
        user_state = state.get_state(request)
        session_state = user_state.get_session_state()
        if session_state == {}:
            prev_state = ""
        else:
            prev_state = session_state['current_state_id']
        # Берём данные пользователя из персистента
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
            if current_state.get_id() == "800":
                if persist_state['previous_state'] == "":
                    previous_state = logic.get_state(session_state["current_state_id"])
                else:
                    previous_state = logic.get_state(persist_state['previous_state'])
                potential_new_state = previous_state.get_next_state(request["request"]["command"])
                if potential_new_state.get_id() != "800":
                    flag = True
                    new_state = potential_new_state

        if new_state.get_id() == "401":
            text, tts = logic.get_random_train()
            response["response"]["text"] = text
            response["response"]["tts"] = tts
        elif new_state.get_id() == "421":
            text, tts = logic.get_random_train()
            response["response"]["text"] = text
            response["response"]["tts"] = tts
        elif new_state.get_id() == "423":
            text, tts = logic.get_recipe()
            response["response"]["text"] = text
            response["response"]["tts"] = tts
        elif new_state.get_id() == "201":
            text, tts = logic.get_recipe()
            response["response"]["text"] = text
            response["response"]["tts"] = tts
        elif new_state.get_id() == "301":
            text, tts = logic.get_first_train()
            response["response"]["text"] = text
            response["response"]["tts"] = tts
        elif new_state.get_id() == "303":
            text, tts = logic.get_second_train()
            response["response"]["text"] = text
            response["response"]["tts"] = tts
        elif new_state.get_id() == "305":
            text, tts = logic.get_third_train()
            response["response"]["text"] = text
            response["response"]["tts"] = tts
        elif new_state.get_id() == "307":
            text, tts = logic.get_forth_train()
            response["response"]["text"] = text
            response["response"]["tts"] = tts
        elif new_state.get_id() == "309":
            text, tts = logic.get_fifth_train()
            response["response"]["text"] = text
            response["response"]["tts"] = tts
        else:
            response["response"]["text"] = new_state.get_text()
            response["response"]["tts"] = new_state.get_tts()
        if new_state.get_id() == "800":
            response["response"]["buttons"] = logic.get_state(session_state["current_state_id"]).get_buttons()
        else:
            response["response"]["buttons"] = new_state.get_buttons()
        response["response"]["card"] = new_state.get_card()
        if new_state.get_id() == "701":
            response["response"]["audio_player"] = new_state.get_audio_player()
        response["response"]["commands"] = new_state.get_commands()

        # if new_state.get_id() == "200" and request["session"]["application"]["application_type"] == "speaker":
        #     new_state = logic.get_state("202")
        #     response["response"]["text"] = new_state.get_text()
        #     response["response"]["tts"] = new_state.get_tts()

        if not new_state.is_end_state():
            session_state["current_state_id"] = new_state.get_id()
            user_state.save_session_state(response)
        else:
            response["response"]["end_session"] = True

        if persist_state == {}:
            persist_state['calories'] = 0
            persist_state['previous_state'] = ""
            user_persist_state.save_session_persist_state(response)
        else:
            if new_state.get_calories() == 9999:
                persist_state['calories'] = None
            elif new_state.get_calories() == 8888:
                persist_state['calories'] = 0
            else:
                if 'calories' in persist_state:
                    persist_state['calories'] += new_state.get_calories()
            if response["response"]["end_session"]:
                persist_state['previous_state'] = None
            else:
                persist_state['previous_state'] = prev_state
            user_persist_state.save_session_persist_state(response)

        if (response["response"]["end_session"] and new_state.get_id() == "900") or (new_state.get_id() == "600"):
            p_state = user_persist_state.get_persist_state()
            if 'calories' in p_state:
                response["response"]["text"] += str(persist_state['calories']) + " калорий"
                response["response"]["tts"] += str(persist_state['calories']) + " калорий"

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
