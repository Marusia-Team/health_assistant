# Логика скилла с переходами
import random
import sys
import psycopg2
sys.path.append('../')
from db.db import new_connection, select_from_fitnes, select_from_recipes, select_from_fitnes_random
connection = psycopg2.connect(user="postgres",
                            password="artem2000",
                            host="127.0.0.1",
                            port="5432",
                            database="health_assistant")
cursor = new_connection(connection)

register_states = {}
global root_state_id
global leaf_state_id


def get_recipe():
    recipe = select_from_recipes(connection, cursor, 'салат')
    text = "Хотели — получите!\n Вкусный и полезный рецепт завтрака!\n" + recipe[3] + \
           "\nХотете ещё рецепт или вернуться?"
    tts = "Хотели — ^получ`ите!^\n Вкусный и полезный рецепт завтрака!\n" + recipe[3] + \
          "\n Хотете ещё рецепт или вернуться?"
    return text, tts


def get_random_train():
    random_train = select_from_fitnes_random(connection, cursor, 'Собственный вес')
    text = "Часть тела, задействованная в упражнении: " + random_train[1].lower() + "\n"\
           "Описание упражнения: " + random_train[4].lower() + "\n"\
           "Мышцы, задействованные в упражнении: " + random_train[5].lower() + "\n" + random_train[3]
    text = [text, "Готовы начать, или хотите другое?"]
    tts = "Часть ^тела^, задействованная в упражнении:\n " + random_train[1].lower() + "\n"\
          "Описание ^упражнения^:\n " + random_train[4].lower() + "\n"\
          "^Мышцы^, задействованные в упражнении:\n " + random_train[5].lower() + \
          "\nГотовы начать или хотите другое?"

    return text, tts


def get_first_train():
    first_train = select_from_fitnes(connection, cursor, 'Собственный вес', "Спина")
    text = "Упражнение №1: упражнение на спину\n" \
           "Описание упражнения: " + first_train[4].lower() + "\n" \
           "Мышцы, задействованные в упражнении: " + first_train[5].lower() + "\n" + first_train[3]
    text = [text, "Готовы начать, или хотите другое?"]
    tts = "Упражнение номер ^один^: упражнение на ^спину^\n" \
          "Описание ^упражнения^:\n " + first_train[4].lower() + "\n" \
          "^Мышцы^, задействованные в упражнении:\n " + first_train[5].lower() + \
          "\nГотовы начать или перейти дальше к следующему упражнению?"

    return text, tts


def get_second_train():
    second_train = select_from_fitnes(connection, cursor, 'Собственный вес', "Грудь")
    text = "Упражнение №2: упражнение на грудь\n" \
           "Описание упражнения: " + second_train[4].lower() + "\n" \
           "Мышцы, задействованные в упражнении: " + second_train[5].lower() + "\n" + second_train[3]
    text = [text, "Готовы начать, или хотите другое?"]
    tts = "Упражнение номер ^два^: упражнение на ^грудь^\n " \
          "Описание ^упражнения^:\n " + second_train[4].lower() + "\n" \
          "^Мышцы^, задействованные в упражнении:\n " + second_train[5].lower() + \
          "\nГотовы начать или перейти дальше к следующему упражнению?"

    return text, tts


def get_third_train():
    third_train = select_from_fitnes(connection, cursor, 'Собственный вес', "Верхние части ног")
    text = "Упражнение №3: упражнение на ноги\n" \
           "Описание упражнения: " + third_train[4].lower() + "\n" \
           "Мышцы, задействованные в упражнении: " + third_train[5].lower() + "\n" + third_train[3]
    text = [text, "Готовы начать, или хотите другое?"]
    tts = "Упражнение номер ^три^: упражнение на ^ноги^\n " \
          "Описание ^упражнения^:\n " + third_train[4].lower() + "\n" \
          "^Мышцы^, задействованные в упражнении:\n " + third_train[5].lower() + \
          "\nГотовы начать или перейти дальше к следующему упражнению?"

    return text, tts


def get_forth_train():
    forth_train = select_from_fitnes(connection, cursor, 'Собственный вес', "Верхние части рук")
    text = "Упражнение №4: упражнение на руки\n" \
           "Описание упражнения: " + forth_train[4].lower() + "\n" \
           "Мышцы, задействованные в упражнении: " + forth_train[5].lower() + "\n" + forth_train[3]
    text = [text, "Готовы начать, или хотите другое?"]
    tts = "Упражнение номер ^четыре^: упражнение на ^руки^\n " \
          "Описание ^упражнения^:\n " + forth_train[4].lower() + "\n" \
          "^Мышцы^, задействованные в упражнении:\n " + forth_train[5].lower() + \
          "\nГотовы начать или перейти дальше к следующему упражнению?"

    return text, tts


def get_fifth_train():
    fifth_train = select_from_fitnes(connection, cursor, 'Собственный вес', "Кардио")
    text = "Упражнение №5: упражнение на спину\n" \
           "Описание упражнения: " + fifth_train[4].lower() + "\n" \
           "Мышцы, задействованные в упражнении: " + fifth_train[5].lower() + "\n" + fifth_train[3]
    text = [text, "Готовы начать, или закончить программу?"]
    tts = "Упражнение номер ^пять^: ^кардио^\n " \
          "Описание ^упражнения^:\n " + fifth_train[4].lower() + "\n" \
          "^Мышцы^, задействованные в упражнении:\n " + fifth_train[5].lower() + \
          "\nГотовы начать или завершить программу?"

    return text, tts


def get_state(state_id):
    return register_states[state_id]


def get_root_state():
    global root_state_id
    return register_states[root_state_id]


def get_leaf_state():
    global leaf_state_id
    return register_states[leaf_state_id]


# переход
class Transition:

    def __init__(self, to_id, synonims):
        self.to_id = to_id
        self.synonims = synonims

    def must_go(self, user_text):
        return user_text in self.synonims

    def get_to_id(self):
        return self.to_id


# состояние пользователя
class State:

    def __init__(self, id, text, transitions, default_transition, tts, buttons=None,
                 calories=0, card=None, commands=None, audio_player=None, is_end=False):
        if audio_player is None:
            audio_player = {}
        if commands is None:
            commands = []
        if card is None:
            card = {}
        if buttons is None:
            buttons = []
        self.id = id
        self.text = text
        self.transitions = transitions
        self.default_transition = default_transition
        self.tts = tts
        self.buttons = buttons
        self.calories = calories
        self.card = card
        self.commands = commands
        self.audio_player = audio_player
        self.is_end = is_end

    def get_next_state(self, user_input):
        for trans in self.transitions:
            if trans.must_go(user_input):
                return get_state(trans.to_id)
        return get_state(self.default_transition)

    def register(self):
        global register_states
        register_states[self.id] = self

    def get_id(self):
        return self.id

    def is_end_state(self):
        return self.is_end

    def get_text(self):
        return self.text

    def get_tts(self):
        return self.tts

    def get_buttons(self):
        return self.buttons

    def get_calories(self):
        return self.calories

    def get_card(self):
        return self.card

    def get_commands(self):
        return self.commands

    def get_audio_player(self):
        return self.audio_player


def init():
    global root_state_id
    global leaf_state_id
    State("100",
          "Привет! Я помогу Вам поддержать себя в хорошей форме, "
          "а также порекомендую вам вкусный и полезный завтрак." 
          "Со мной никакой фитнес-клуб не нужен! "
          "Вы можете выбрать тренировочную программу из нескольких упражнений,"
          " случайное упражнение или полезный рецепт, а также следить за своей статистикой. Хотите начать?",
          [Transition("901", ["нет", "не хочу"])],
          "101",
          "^Привет!^ Я помогу Вам поддержать себя в хорошей форме,"
          "а также порекомендую вам вкусный и полезный завтрак. \n"
          "Со мной никакой фитнес-клуб не нужен! "
          "Вы можете выбрать тренировочную программу из нескольких упражнений,"
          " случайное упражнение или полезный рецепт, а также следить за своей статистикой. Хотите начать?",
          [
              {
                  "title": "Да!",
                  "payload": {
                      "action": "да"
                  }
              },
              {
                  "title": "Нет :(",
                  "payload": {
                      "action": "нет"
                  }
              }
          ]).register()

    # Нужно добавить переходы в ветки
    State("101",
          "Скажите «Программа» для запуска тренировочной программы\n\n"
          "«Упражнение» для выбора случайного упражнения\n\n«Завтрак» для выбора лёгкого и полезного блюда\n\n"
          "«Счёт» чтобы запустить отсчёт для своего упражнения\n\n"
          "«Статистика» чтобы узнать свой прогресс\n\n"
          "«тест» для теста возможностей\n\n чтобы выйти скажите «Завершить»",
          [
              Transition("200", ["завтрак", "блюдо", "блюда", "рецепт"]),
              Transition("300", ["программа", "программу"]),
              Transition("400", ["упражнение", "упражнения"]),
              Transition("500", ["счет", "счёт"]),
              Transition("600", ["статистика"]),
              Transition("700", ["тест"]),
              Transition("900", ["завершить"])
          ],
          "800",
          "Скажите ^«Программа»^ для запуска тренировочной программы, \n"
          "^«упражнение»^ для выбора случайного упражнения, \n"
          "^«салат»^ для выбора лёгкого и полезного блюда на завтрак, \n"
          "^«Счёт»^ чтобы запустить отсчёт для своего упражнения, \n"
          "^«Статистика»^ чтобы узнать свой прогресс, \n"
          "^«тэст»^ для тэста возможностей, чтобы выйти скажите «Завершить»",
          [
              {
                  "title": "Программа",
                  "payload": {
                      "action": "программа"
                  }
              },
              {
                  "title": "Упражнение",
                  "payload": {
                      "action": "упражнение"
                  }
              },
              {
                  "title": "Завтрак",
                  "payload": {
                      "action": "завтрак"
                  }
              },
              {
                  "title": "Счёт",
                  "payload": {
                      "action": "счет"
                  }
              },
              {
                  "title": "Статистика",
                  "payload": {
                      "action": "статистика"
                  }
              },
              {
                  "title": "Тест",
                  "payload": {
                      "action": "тест"
                  }
              },
              {
                  "title": "Завершить",
                  "payload": {
                      "action": "завершить"
                  }
              }
          ]).register()

    # Рецепт
    State("200",
          "Завтрак - это самый важный приём пищи и вершина кулинарного искусства! Хотите услышать рецепт завтрака, "
          "чтобы замечательно начать этот день? Или вернуться в меню?",
          [Transition("101", ["вернуться", "меню"]),
           Transition("201", ["да"])],
          "800",
          "^Завтрак^ - это самый важный приём пищи и вершина кулинарного искусства! Хотите услышать рецепт завтрака, "
          "чтобы замечательно начать этот день? Или вернуться в меню?",
          buttons=[
              {
                  "title": "Да",
                  "payload": {
                      "action": "да"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ]).register()

    State("201",  "",
          [
              Transition("101", ["вернуться"]),
              Transition("201", ["ещё", "еще"])
          ],
          "800",
          "",
          buttons=[
              {
                  "title": "Ещё",
                  "payload": {
                      "action": "еще"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ],
          card={
              "type": "BigImage",
              "image_id": 457239018
          }
          ).register()

    # speaker
    State("202", "Спросите меня об этом лучше в приложении, или запустите рецепты сказав мне «Давай готовить», "
                 "но сначала договорим о тренировке. Скажите «Вернуться», чтобы вернуться в меню или "
                 "«Завершить», чтобы выйти",
          [
              Transition("101", ["вернуться"]),
              Transition("301", ["завершить"])
          ], "800",
          "Спросите меня об этом лучше в приложении, или запустите рецепты сказав мне «Давай готовить», "
          "но сначала договорим о тренировке. Скажите «Вернуться», чтобы вернуться в меню или "
          "«Завершить», чтобы выйти"
          ).register()

    # Программа
    State("300",
          "Я расскажу Вам пять случайных упражнений на разные группы мышц, каждое упражнение занимает "
          "тридцать секунд. Чтобы вернуться в меню во время программы скажите «Вернуться». Начать программу?",
          [
              Transition("101", ["вернуться"]),
              Transition("301", ["начать", "да"])
          ],
          "800",
          "Я расскажу Вам ^пять^ случайных упражнений на разные группы мышц, каждое упражнение занимает "
          "тридцать секунд. Чтобы вернуться в меню во время программы скажите ^«Вернуться»^.\nНачать программу?",
          buttons=[
              {
                  "title": "Начать",
                  "payload": {
                      "action": "начать"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ]
          ).register()

    State("301", "",
          [
              Transition("101", ["вернуться"]),
              Transition("302", ["начать", "да"]),
              Transition("303", ["следующее", "дальше"])
          ],
          "800", "",
          buttons=[
              {
                  "title": "Начать",
                  "payload": {
                      "action": "начать"
                  }
              },
              {
                  "title": "Дальше",
                  "payload": {
                      "action": "дальше"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ],
          card={
              "type": "BigImage",
              "image_id": 457239020
          }
          ).register()

    State("302",
          ["Начинаем!", "Скажите «Дальше» чтобы перейти к следующему упражнению, «Вернуться» чтобы вернуться в меню"],
          [
              Transition("101", ["вернуться"]),
              Transition("303", ["дальше", "следующее"])
          ],
          "800",
          "^Начинаем!^ \n <speaker audio_vk_id=2000512031_456239035> "
          "Скажите «Дальше» чтобы перейти к следующему упражнению, «Вернуться» чтобы вернуться в меню",
          [
              {
                  "title": "Дальше",
                  "payload": {
                      "action": "дальше"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ],
          calories=4,
          card={
              "type": "BigImage",
              "image_id": 457239024
          }
          ).register()

    State("303", "",
          [
              Transition("101", ["вернуться"]),
              Transition("304", ["начать", "да"]),
              Transition("305", ["следующее", "дальше"])
          ],
          "800", "",
          buttons=[
              {
                  "title": "Начать",
                  "payload": {
                      "action": "начать"
                  }
              },
              {
                  "title": "Дальше",
                  "payload": {
                      "action": "дальше"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ],
          card={
              "type": "BigImage",
              "image_id": 457239022
          }
          ).register()

    State("304",
          ["Начинаем!", "Скажите «Дальше» чтобы перейти к следующему упражнению, «Вернуться» чтобы вернуться в меню"],
          [
              Transition("101", ["вернуться"]),
              Transition("305", ["дальше", "следующее"])
          ],
          "800",
          "^Начинаем!^ \n <speaker audio_vk_id=2000512031_456239035> "
          "Скажите «Дальше» чтобы перейти к следующему упражнению, «Вернуться» чтобы вернуться в меню",
          [
              {
                  "title": "Дальше",
                  "payload": {
                      "action": "дальше"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ],
          calories=5,
          card={
              "type": "BigImage",
              "image_id": 457239024
          }
          ).register()

    State("305", "",
          [
              Transition("101", ["вернуться"]),
              Transition("306", ["начать", "да"]),
              Transition("307", ["следующее", "дальше"])
          ],
          "800", "",
          buttons=[
              {
                  "title": "Начать",
                  "payload": {
                      "action": "начать"
                  }
              },
              {
                  "title": "Дальше",
                  "payload": {
                      "action": "дальше"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ],
          card={
              "type": "BigImage",
              "image_id": 457239021
          }
          ).register()

    State("306",
          ["Начинаем!", "Скажите «Дальше» чтобы перейти к следующему упражнению, «Вернуться» чтобы вернуться в меню"],
          [
              Transition("101", ["вернуться"]),
              Transition("307", ["дальше", "следующее"])
          ],
          "800",
          "^Начинаем!^ \n <speaker audio_vk_id=2000512031_456239035> "
          "Скажите «Дальше» чтобы перейти к следующему упражнению, «Вернуться» чтобы вернуться в меню",
          [
              {
                  "title": "Дальше",
                  "payload": {
                      "action": "дальше"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ],
          calories=6,
          card={
              "type": "BigImage",
              "image_id": 457239024
          }
          ).register()

    State("307", "",
          [
              Transition("101", ["вернуться"]),
              Transition("308", ["начать", "да"]),
              Transition("309", ["следующее", "дальше"])
          ],
          "800", "",
          buttons=[
              {
                  "title": "Начать",
                  "payload": {
                      "action": "начать"
                  }
              },
              {
                  "title": "Дальше",
                  "payload": {
                      "action": "дальше"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ],
          card={
              "type": "BigImage",
              "image_id": 457239023
          }
          ).register()

    State("308",
          ["Начинаем!", "Скажите «Дальше» чтобы перейти к следующему упражнению, «Вернуться» чтобы вернуться в меню"],
          [
              Transition("101", ["вернуться"]),
              Transition("309", ["дальше", "следующее"])
          ],
          "800",
          "^Начинаем!^ \n <speaker audio_vk_id=2000512031_456239035> "
          "Скажите «Дальше» чтобы перейти к следующему упражнению, «Вернуться» чтобы вернуться в меню",
          [
              {
                  "title": "Дальше",
                  "payload": {
                      "action": "дальше"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ],
          calories=7,
          card={
              "type": "BigImage",
              "image_id": 457239024
          }
          ).register()

    State("309", "",
          [
              Transition("101", ["вернуться"]),
              Transition("310", ["начать", "да"]),
              Transition("311", ["завершить"])
          ],
          "800", "",
          buttons=[
              {
                  "title": "Начать",
                  "payload": {
                      "action": "начать"
                  }
              },
              {
                  "title": "Завершить",
                  "payload": {
                      "action": "завершить"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ],
          card={
              "type": "BigImage",
              "image_id": 457239019
          }
          ).register()

    State("310",
          ["Начинаем!", "Скажите «Завершить» чтобы завершить тренировочную программу, "
                        "«Вернуться» чтобы вернуться в меню"],
          [
              Transition("101", ["вернуться"]),
              Transition("311", ["дальше", "следующее"])
          ],
          "800",
          "^Начинаем!^ \n <speaker audio_vk_id=2000512031_456239035> "
          "Скажите «Завершить» чтобы завершить тренировочную программу, «Вернуться» чтобы вернуться в меню",
          [
              {
                  "title": "Завершить",
                  "payload": {
                      "action": "завершить"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ],
          calories=4,
          card={
              "type": "BigImage",
              "image_id": 457239024
          }
          ).register()

    State("311", "Вы закончили тренировочную программу. Так держать! Хотите запустить "
                 "следующую тренировочную программу или завершить пока что?",
          [
              Transition("101", ["завершить"]),
              Transition("300", ["следующее", "следующую"])
          ], "800",
          "Вы закончили тренировочную программу. Так держать! Хотите запустить "
          "следующую тренировочную программу или завершить пока что?",
          buttons=[
              {
                  "title": "Следующую",
                  "payload": {
                      "action": "следующую"
                  }
              },
              {
                  "title": "Завершить",
                  "payload": {
                      "action": "завершить"
                  }
              }
          ]
          ).register()

    # Упражнение
    State("400",
          "Вам будет предложено одно упражнение длительностью 30 секунд. "
          "Скажите ^«Да»^, если готовы начать или ^«Нет»^, чтобы вернуться в меню выбора",
          [Transition("101", ["нет", "не хочу"]),
           Transition("401", ["да"])
           ], "800", "Вам будет предложено одно упражнени.\n Скажите да, если готовы начать или нет, "
                     "чтобы вернуться в меню выбора.",
          [
              {
                  "title": "Да",
                  "payload": {
                      "action": "да"
                  }
              },
              {
                  "title": "Нет",
                  "payload": {
                      "action": "нет"
                  }
              }
          ]).register()

    # Можно вставить картинок с упражнениями
    State("401",
          "",
          [Transition("101", ["нет", "не хочу"]),
           Transition("410", ["да", "начать", "готов"]),
           Transition("401", ["другое"])
           ], "800", "",
          [
              {
                  "title": "Да",
                  "payload": {
                      "action": "да"
                  }
              },
              {
                  "title": "Нет",
                  "payload": {
                      "action": "нет"
                  }
              },
              {
                  "title": "Другое",
                  "payload": {
                      "action": "другое"
                  }
              }

          ]).register()

    State("410",
          ["Начинаем!", "Скажите «Ещё» чтобы выбрать новое упражение, «Нет» чтобы выйти в меню"],
          [
              Transition("101", ["нет", "не хочу"]),
              Transition("401", ["ещё", "еще", "Еще", "Ещё"])
          ],
          "800",
          "^Начинаем!^ \n <speaker audio_vk_id=2000512031_456239035> "
          "Скажите «Ещё» чтобы выбрать новое упражнение, «Нет» чтобы выйти в меню",
          [
              {
                  "title": "Ещё",
                  "payload": {
                      "action": "еще"
                  }
              },
              {
                  "title": "Нет",
                  "payload": {
                      "action": "нет"
                  }
              }
          ],
          calories=7,
          card={
              "type": "BigImage",
              "image_id": 457239024
          }
          ).register()

    # Отсчёт
    State("500", "У вас уже есть упражнение?! ШТОШ... Я могу посчитать тогда для вас! "
                 "Скажите «Начать» чтобы начать отсчёт или «Вернуться» чтобы вернуться в меню",
          [
              Transition("501", ["начать"]),
              Transition("101", ["вернуться"])
          ], "800",
          "У вас уже есть упражнение?! ^Чтож^ \n\n Я могу посчитать тогда для вас! "
          "Скажите «Начать» чтобы начать отсчёт или «Вернуться» чтобы вернуться в меню",
          buttons=[
              {
                  "title": "Начать",
                  "payload": {
                      "action": "начать"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ]).register()

    State("501",
          ["Начинаем!", "Скажите «Ещё» чтобы посчитать заново, «Отдых», чтобы отдохнуть 30 секунд, "
                        "«Вернуться» чтобы вернуться в меню"],
          [
              Transition("101", ["вернуться"]),
              Transition("502", ["отдых"]),
              Transition("501", ["ещё", "еще", "Еще", "Ещё"])
          ],
          "800",
          "^Начинаем!^ \n <speaker audio_vk_id=2000512031_456239035> "
          "Скажите «Ещё» чтобы посчитать заново, «Отдых», чтобы отдохнуть 30 секунд, "
          "«Вернуться» чтобы выйти в меню",
          [
              {
                  "title": "Ещё",
                  "payload": {
                      "action": "еще"
                  }
              },
              {
                  "title": "Отдых",
                  "payload": {
                      "action": "отдых"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ],
          calories=7,
          card={
              "type": "BigImage",
              "image_id": 457239024
          }
          ).register()

    State("502",
          ["Отдыхаем!", "Скажите «Ещё» чтобы отдохнуть заново, «Начать» чтобы начать отсчёт, "
                        "«Вернуться» чтобы вернуться в меню"],
          [
              Transition("101", ["вернуться"]),
              Transition("501", ["начать"]),
              Transition("502", ["ещё", "еще", "Еще", "Ещё"])
          ],
          "800",
          "^Отдыхаем!^ \n <speaker audio_vk_id=2000512031_456239035> "
          "Скажите «Ещё» чтобы отдохнуть заново, «Начать» чтобы начать отсчёт, "
          "«Вернуться» чтобы вернуться в меню",
          [
              {
                  "title": "Ещё",
                  "payload": {
                      "action": "еще"
                  }
              },
              {
                  "title": "Начать",
                  "payload": {
                      "action": "начать"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ],
          card={
              "type": "BigImage",
              "image_id": 457239024
          }
          ).register()

    # Статистика
    State("600", "Для удаления статистики скажите «Удалить», чтобы вернуться в меню скажите «Вернуться» "
                 "\n Всего потрачено: ",
          [
              Transition("601", ["удалить"]),
              Transition("101", ["вернуться"])
          ],
          "800",
          "Для удаления статистики скажите «Удалить», чтобы вернуться в меню скажите «Вернуться» "
          "\n Всего потрачено: ",
          buttons=[
              {
                  "title": "Удалить",
                  "payload": {
                      "action": "удалить"
                  }
              },
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              }
          ]
          ).register()

    State("601",
          "Статистика удалена\n\nСкажите «Вернуться» чтобы вернуться в меню или «Завершить» чтобы выйти",
          [
              Transition("900", ["завершить"]),
              Transition("101", ["вернуться"])
           ],
          "800",
          "Статистика удалена\n\nСкажите ^«Вернуться»^ чтобы вернуться в меню или ^«Завершить»^ чтобы выйти",
          [
              {
                  "title": "Вернуться",
                  "payload": {
                      "action": "вернуться"
                  }
              },
              {
                  "title": "Завершить",
                  "payload": {
                      "action": "завершить"
                  }
              }
          ],
          calories=8888
          ).register()

    State("700", "Состояние для теста",
          [
              Transition("900", ["нет", "не хочу"]),
              Transition("101", ["ещё", "еще", "Еще", "Ещё"]),
              Transition("701", ["плеер"]),
              Transition("702", ["гифка"]),
              Transition("703", ["удалить статистику"])
           ], "800", "",
          [
              {
                  "title": "Нет",
                  "payload": {
                      "action": "нет"
                  }
              },
              {
                  "title": "Ещё",
                  "payload": {
                      "action": "еще"
                  }
              },
              {
                  "title": "Плеер",
                  "payload": {
                      "action": "плеер"
                  }
              },
              {
                  "title": "Удалить статистику",
                  "payload": {
                      "action": "удалить"
                  }
              },
              {
                  "title": "Гифка",
                  "payload": {
                      "action": "гифка"
                  }
              }
          ]
          ).register()

    State("701", "Аудиоплеер",
          [
              Transition("700", ["Дальше"])
          ], "800", "Аудиоплеер", buttons=
          [
              {
                  "title": "Дальше",
                  "payload": {
                      "action": "Дальше"
                  }
              }
          ],
          audio_player={
              "seek_track": 0,
              "seek_second": 0,
              "playlist": [
                  {
                      "stream": {
                          "track_id": "2000512031_456239035",
                          "source_type": "vk",
                          "source": "2000512031_456239035"
                      },
                      "meta": {
                          "sub_title": "Artem Nikolaev",
                          "title": "The best ever song",
                      }
                  }
              ]
          }
          ).register()

    State("702", "Гифка",
          [
              Transition("700", ["Дальше"])
          ], "800", "Аудиоплеер", buttons=
          [
              {
                  "title": "Дальше",
                  "payload": {
                      "action": "Дальше"
                  }
              }
          ], card={
              "type": "BigImage",
              "image_url": "http://d205bpvrqc9yn1.cloudfront.net/0859.gif"
          }
          ).register()

    # Зануление калорий с удалением из персистента
    State("703",
          "Зануляю калории с удалением",
          [Transition("901", ["нет", "не хочу"])],
          "901",
          "Зануляю калории",
          [
              {
                  "title": "Нет",
                  "payload": {
                      "action": "нет"
                  }
              }
          ],
          calories=9999
          ).register()

    # ситуативный unknown
    State("800", "Ответ как-то сложноват для меня, попробуйте снова, пожалуйста", [],
          "900", "Ответ как-то сложноват для меня \n попробуйте снова ^по`жалуйста^").register()

    # хватит
    State("900", f'Буду рада видеть Вас снова! Всего потрачено: ', [], None,
          "Буду рада видеть Вас снова! Всего потрачено: ",
          is_end=True).register()

    State("901", "До скорых встречь!", [], None, "До скорых встречь!", is_end=True).register()

    root_state_id = "100"
    leaf_state_id = "101"


init()
