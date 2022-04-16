# Логика скилла с переходами

register_states = {}


def get_state(state_id):
    return register_states[state_id]


def get_root_state():
    global root_state_id
    return register_states[root_state_id]


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

    def __init__(self, id, text, transitions, default_transition, is_end=False):
        self.id = id
        self.text = text
        self.transitions = transitions
        self.default_transition = default_transition
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

def init():
    global root_state_id
    State("100", "Привет! Я помогу Вам поддержать себя в хорошей форме, "
                 "а также порекомендую вам вкусную и полезную еду." 
                 "Со мной никакой фитнес-клуб не нужен! "
                 "Вы можете выбрать тренировочную программу из нескольких упражнений,"
                 " случайное упражнение или полезный рецепт. Хотите начать?",
          [Transition("900", ["нет", "не хочу", "хватит"])], "101").register()

    State("101", "Скажите «Программа» для запуска тренировочной программы,"
                 "«упражнение» для выбора случайного упражнения и «рецепт» для выбора блюда.",
          [Transition("900", ["нет", "не хочу", "хватит"])], "102").register()

    # Рецепт
    State("200", "Какой рацион выберите: для похудения или для набора массы?",
          [Transition("900", ["нет", "не хочу", "хватит"]),
           Transition("201", ["похудение"]),
           Transition("202", ["набор"])], "800").register()

    State("201", "", [], "800").register()

    State("202", "", [], "800").register()

    # Программа
    State("300", "Я расскажу Вам пять упражнений, каждое упражнение занимает "
                 "тридцать секунд активности и десять сукунд отдыха. Начать программу или вернуться в меню?",
          [Transition("900", ["нет", "не хочу", "хватит"]),
           Transition("101", ["вернутся"]),
           Transition("301", ["Начать"])], "800").register()

    State("301", "", [], "800").register()

    # Упражнение
    State("400", "", [], "800").register()

    # Считаю баранов
    State("500", "Считаю баранов!\n"
                 "Раз\n Два\n Три\n Четыре\n Пять\n Шесть\n Семь\n Восемь\n Девять\n Десять\n "
                 "Спокойной ночи", [Transition("900", ["нет", "не хочу", "хватит"])], "102").register()

    # unknown
    State("102", "Не поняла, повторите пожалуйста. Скажите «Программа» для запуска тренировочной программы,"
                 "«упражнение» для выбора случайного упражнения и «рецепт» для выбора блюда.",
          [Transition("900", ["нет", "не хочу", "хватит"])], "102").register()

    # ситуативный unknown
    State("800", "", [], "800").register()

    # хватит
    State("900", "Буду рада видеть Вас снова!", [], None, is_end=True).register()

#Сделать дефолтное состояние, в которое сваливаться, если не распознать, для этапа, чтобы не вылетать из текущей логики
    # можно доставать следующее состояние из регистра состояний

    root_state_id = "100"


init()