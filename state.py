# Сохранение состояний пользователя

class UserState:

    def __init__(self, request):
        self.session_state = request["state"]["session"]

    def get_session_state(self):
        return self.session_state

    def save_session_state(self, response):
        response["session_state"] = self.session_state


def get_state(request):
    return UserState(request)


class UserPersistState:

    def __init__(self, request):
        self.persist_state = request["state"]["user"]

    def get_persist_state(self):
        return self.persist_state

    def save_session_persist_state(self, response):
        print(self.persist_state)
        response["user_state_update"] = self.persist_state


def get_persist_state(request):
    return UserPersistState(request)
