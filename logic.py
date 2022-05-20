# Логика скилла с переходами
import random

register_states = {}
train = {
    1: "Салат с осьминогом",
    2: "Салат с морепродуктами",
    3: "Салат из огурцов и курицы"
}
global root_state_id
global leaf_state_id


def get_random_train():
    random_num = random.randint(1, 3)
    random_train = train[random_num]
    return random_train


def get_first_train():
    first_train = None
    return first_train


def get_second_train():
    second_train = None
    return second_train


def get_third_train():
    third_train = None
    return third_train


def get_forth_train():
    forth_train = None
    return forth_train


def get_fifth_train():
    fifth_train = None
    return fifth_train


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
          "а также порекомендую вам вкусный и полезный салат." 
          "Со мной никакой фитнес-клуб не нужен! "
          "Вы можете выбрать тренировочную программу из нескольких упражнений,"
          " случайное упражнение или полезный рецепт. Хотите начать?",
          [Transition("900", ["нет", "не хочу"])],
          "101",
          "^Привет!^ Я помогу Вам поддержать себя в хорошей форме,"
          "а также порекомендую вам вкусный и полезный салат. \n"
          "Со мной никакой фитнес-клуб не нужен! "
          "Вы можете выбрать тренировочную программу из нескольких упражнений,"
          " случайное упражнение или полезный рецепт. Хотите начать?",
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
          "Скажите «Программа» для запуска тренировочной программы, "
          "«упражнение» для выбора случайного упражнения, «Салат» для выбора лучшего блюда в мире, "
          "«занулить» для того, чтобы сбросить калории и «обнулить», чтобы обнулить калории, "
          "«тест» для теста возможностей",
          [
              Transition("900", ["нет", "не хочу"]),
              Transition("200", ["салат", "блюдо", "блюда", "рецепты"]),
              Transition("300", ["программа", "программу"]),
              Transition("400", ["упражнение", "упражнения"]),
              Transition("500", ["занулить"]),
              Transition("600", ["обнуление"]),
              Transition("700", ["тест"])
          ],
          "800",
          "Скажите «Программа» для запуска тренировочной программы,"
          "«упражнение» для выбора случайного упражнения, «салат» для выбора лучшего блюда в мире и "
          "«занулить» для того, чтобы сбросить калории, «обнулить», чтобы обнулить калории, "
          "«тест» для теста возможностей",
          [
              {
                  "title": "Салат",
                  "payload": {
                      "action": "салат"
                  }
              },
              {
                  "title": "Программма",
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
                  "title": "Занулить",
                  "payload": {
                      "action": "занулить"
                  }
              },
              {
                  "title": "Обнуление",
                  "payload": {
                      "action": "обнуление"
                  }
              },
              {
                  "title": "Тест",
                  "payload": {
                      "action": "тест"
                  }
              },
              {
                  "title": "Нет",
                  "payload": {
                      "action": "нет"
                  }
              }
          ]).register()

    # Рецепт
    State("200",
          "Салат - это вершина кулинарного искусства! Хотите услышать рецепт салата?",
          [Transition("101", ["вернуться"]),
           Transition("201", ["Да"])],
          "800",
          "Какой рацион выберите: для похудения или для набора массы?",
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

    State("201",  text="", transitions=[
        Transition("101", ["вернуться"]),
        Transition("202", ["ещё", "еще"])
    ], default_transition="800", tts="Слоныыыыыыыыы", buttons=[
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
    ]).register()

    # Программа
    State("300",
          "Я расскажу Вам пять упражнений, каждое упражнение занимает "
          "тридцать секунд активности и десять сукунд отдыха. Начать программу или вернуться в меню?",
          [Transition("900", ["нет", "не хочу"]),
           Transition("101", ["вернутся"]),
           Transition("301", ["Начать"])],
          "800",
          "Я расскажу Вам пять упражнений, каждое упражнение занимает "
          "тридцать секунд активности и десять сукунд отдыха. Начать программу или вернуться в меню?",
          ).register()

    State("301", "", [], "800", "Слоныыыыыыыыы").register()

    # Упражнение
    # Для временного решения можно сделать выбор из всех упражнений, дальше можно в
    # аппе выбирать из транзишеннов рандомное
    # по-хорошему надо здесь ходить в бд и забираться массив номеров(?) упражнений,
    # потом выбирать рандомное и забирать его из бд
    State("400",
          "Вам будет предложено одно упражнение длительностью 30 секунд. "
          "Скажите «Да», если готовы начать или «Нет», чтобы вернуться в меню выбора",
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
          ["Упражнение «Планка». Займите упор лёжа на предплечьях.", "Готовы?"],
          [Transition("101", ["нет", "не хочу"]),
           Transition("410", ["да"])
           ], "800", "Упражнение «Планка». Займите упор лёжа на предплечьях. \n\nГотовы?",
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

    State("410",
          ["Начинаем!", "Скажите «Ещё» чтобы выбрать новое упражение, «Нет» чтобы выйти в меню"],
          [
              Transition("101", ["нет", "не хочу"]),
              Transition("401", ["ещё", "еще", "Еще", "Ещё"])
          ],
          "800",
          "Начинаем! \n <speaker audio_vk_id=2000512031_456239035> "
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
          calories=10,
          card={
              "type": "BigImage",
              "image_id": 457239017
          }
          ).register()

    # Зануление калорий с удалением из персистента
    State("500",
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

    # Простое зануление
    State("600",
          "Зануляю калории просто, «Нет» - чтобы выйти из функции, «Ещё» - вернуться в меню",
          [
              Transition("900", ["нет", "не хочу"]),
              Transition("101", ["ещё", "еще", "Еще", "Ещё"])
           ],
          "800",
          "Зануляю калории",
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
              }
          ],
          calories=8888
          ).register()

    State("700", "Состояние для теста",
          [
              Transition("900", ["нет", "не хочу"]),
              Transition("101", ["ещё", "еще", "Еще", "Ещё"]),
              Transition("701", ["плеер"]),
              Transition("702", ["гифка"])
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

    # ситуативный unknown
    State("800", "Ответ как-то сложноват для меня, попробуйте снова, пожалуйста", [],
          "900", "Ответ как-то сложноват для меня \n попробуйте снова ^по`жалуйста^").register()

    # хватит
    State("900", f'Буду рада видеть Вас снова! Всего потрачено: ', [], None, "конец", is_end=True).register()

    State("901", "До скорых встречь!", [], None, "конец", is_end=True).register()

    # Сделать дефолтное состояние, в которое сваливаться, если не распознать, для этапа,
    # чтобы не вылетать из текущей логики
    # можно доставать следующее состояние из регистра состояний

    root_state_id = "100"
    leaf_state_id = "101"


init()
