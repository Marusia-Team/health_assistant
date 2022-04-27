# Логика скилла с переходами

register_states = {}
global root_state_id
global leaf_state_id


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
                 calories=0, card=None, commands=None, is_end=False):
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


def init():
    global root_state_id
    global leaf_state_id
    State("100",
          "Привет! Я помогу Вам поддержать себя в хорошей форме, "
          "а также порекомендую вам вкусную и полезную еду." 
          "Со мной никакой фитнес-клуб не нужен! "
          "Вы можете выбрать тренировочную программу из нескольких упражнений,"
          " случайное упражнение или полезный рецепт. Хотите начать?",
          [Transition("900", ["нет", "не хочу"])],
          "101",
          "^Привет!^ Я помогу Вам поддержать себя в хорошей форме,"
          "а также порекомендую вам вкусную и полезную еду. \n"
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
          "«упражнение» для выбора случайного упражнения, «рецепт» для выбора блюда и "
          "«бараны» для того, чтобы их посчитать и заснуть!",
          [Transition("900", ["нет", "не хочу"]),
           Transition("200", ["рецепт", "блюдо", "блюда", "рецепты"]),
           Transition("300", ["программа", "программу"]),
           Transition("400", ["упражнение", "упражнения"]),
           Transition("500", ["баран", "бараны", "баранов"])
           ],
          "102",
          "Скажите «Программа» для запуска тренировочной программы,"
          "«упражнение» для выбора случайного упражнения, «рецепт» для выбора блюда и "
          "«бараны» для того, чтобы их посчитать и заснуть!",
          [
              {
                  "title": "Рецепт",
                  "payload": {
                      "action": "рецепт"
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
                  "title": "Бараны",
                  "payload": {
                      "action": "баран"
                  }
              },
              {
                  "title": "Нет",
                  "payload": {
                      "action": "не хочу"
                  }
              }
          ]).register()

    # Рецепт
    State("200",
          "Какой рацион выберите: для похудения или для набора массы или вернуться в меню?",
          [Transition("900", ["нет", "не хочу"]),
           Transition("101", ["вернутся"]),
           Transition("201", ["похудение"]),
           Transition("202", ["набор"])],
          "800",
          "Какой рацион выберите: для похудения или для набора массы?",
          ).register()

    State("201", "", [], "800", "Слоныыыыыыыыы").register()

    State("202", "", [], "800", "Слоныыыыыыыыы").register()

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
    State("400",
          "Вам будет предложено одно упражнени длительностью 30 секунд. "
          "Скажите да, если готовы начать или нет, чтобы вернуться в меню выбора",
          [Transition("101", ["нет", "не хочу"]),
           Transition("401", ["да"])
           ], "102", "Вам будет предложено одно упражнени.\n Скажите да, если готовы начать или нет, "
                     "чтобы вернуться в меню выбора.").register()

    # Можно вставить картинок с упражнениями
    State("401",
          ["Упражнение «Платка». Займите упор лёжа на предплечьях.", "Готовы?"],
          [Transition("101", ["нет", "не хочу"]),
           Transition("410", ["да"])
           ], "102", "Упражнение «Планка». Займите упор лёжа на предплечьях. \n\nГотовы?").register()

    State("410",
          ["Начинаем!", "Скажите «Ещё» чтобы выбрать новое упражение, «Нет» чтобы выйти в меню"],
          [
              Transition("101", ["нет", "не хочу"]),
              Transition("400", ["ещё, еще"])
          ],
          "800",
          "Начинаем! \n <speaker audio_vk_id=2000512031_456239035> "
          "Скажите «Ещё» чтобы выбрать новое упражнение, «Нет» чтобы выйти в меню",
          calories=50,
          card={
              "type": "BigImage",
              "image_id": 457239017
          }
          ).register()

    # Считаю баранов
    State("500",
          "Считаю баранов!\n"
          "Спокойной ночи",
          [Transition("900", ["нет", "не хочу"])],
          "900",
          "Счёт баранов",
          card={
                  "type": "BigImage",
                  "image_url": "https://cdn.ananasposter.ru/image/cache/catalog/poster/anime/81/17291-1000x830.jpg"
          }
          ).register()

    # unknown
    State("102",
          "Не поняла, повторите пожалуйста. Скажите «Программа» для запуска тренировочной программы,"
          "«упражнение» для выбора случайного упражнения, «рецепт» для выбора блюда или "
          "«бараны» для того, чтобы их посчитать и заснуть!",
          [Transition("200", ["рецепт", "блюдо", "блюда", "рецепты"]),
           Transition("300", ["программа", "программу"]),
           Transition("400", ["упражнение", "упражнения"]),
           Transition("500", ["баран", "бараны", "баранов"])],
          "900",
          "Не поняла, повторите пожалуйста. Скажите «Программа» для запуска тренировочной программы,"
          "«упражнение» для выбора случайного упражнения и «рецепт» для выбора блюда.",
          ).register()

    # ситуативный unknown
    State("800", "Слоныыыыыыыыы", [], "900", "Слоныыыыыыыыы").register()

    # хватит
    State("900", f'Буду рада видеть Вас снова! Всего потрачено: ', [], None, "конец", is_end=True).register()

    # Сделать дефолтное состояние, в которое сваливаться, если не распознать, для этапа,
    # чтобы не вылетать из текущей логики
    # можно доставать следующее состояние из регистра состояний

    root_state_id = "100"
    leaf_state_id = "101"


init()
