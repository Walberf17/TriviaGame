__version__ = "0.1.2"

"""
A trivia game
"""

# import from kivy
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivy.animation import Animation
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton, MDRectangleFlatButton
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.screenmanager import SlideTransition as Trans
from kivy.uix.widget import Widget

# other imports
import random
from functools import partial
import os
# from questions import QUESTIONS

# Variables
TOTAL_POINTS = 0
TOTAL_QUESTIONS = 0
os.environ['KIVY_ORIENTATION'] = 'Portrait'

QUESTIONS = [

    {
        "text": "Qual o menor Átomo que exite?",
        "options": [
            "Hidrogênio",
            "Oxigênio",
            "Carbono",
            "Sódio"
        ],
        "image": None
    },

    {
        "text": "Qual o Átomo mais comum?",
        "options": [
            "Hidrogênio",
            "Oxigênio",
            "Carbono",
            "Sódio"
        ],
        "image": None
    },

    {
        "text": "Qual a ligação mais forte?",
        "options": [
            "Iônica",
            "Covalente",
            "Molecular",
        ],
        "image": None
    },

    {
        "text": "Qual a Fórmula da Água?",
        "options": [
            "H_2 O",
            "HO",
            "H2CO3",
            "NaCl"
        ],
        "image": None
    },

    {
        "text": "Quantos Átomos existem na formula da água?",
        "options": [
            3,
            4,
            2,
            1
        ],
        "image": None
    },

    {
        "text": "Qual o Átomo mais importante para Química Orgânica?",
        "options": [
            "Carbono",
            "Oxigênio",
            "Hidrogênio",
            "Sódio",
        ],
        "image": None
    },

    {
        "text": "O grupo -OH ligado a um carbono tetraédrico é típico de qual grupo funcional?",
        "options": [
            "Álcool",
            "Cetona",
            "Ácido Carboxílico",
            "Enol",
        ],
        "image": None
    },

    {
        "text": "O que une as moléculas de água?",
        "options": [
            "Ligação de Hidrogênio",
            "Vander Walls",
            "Ligação Iônica",
            "Ligação Metálica",
        ],
        "image": None
    },

]


# Screens
class MainScreen(Screen):
    def __init__(self, widget, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(widget)


####################### Windows
""""""


### Main Question Window
class Answer(MDRelativeLayout):
    def __init__(self, letter, text, right, option_grid, **kwargs):
        super().__init__(**kwargs)
        self.option_grid = option_grid

        self.letter = MDLabel(text=f" {letter})", valign="center", font_style="H5", max_lines=1, size_hint_x=.1)

        self.lbl = MDLabel(text=text, valign="center", font_style="H5", size_hint_x=.9)

        line = MDGridLayout(cols=2)

        line.add_widget(self.letter)

        line.add_widget(self.lbl)
        self.btn = MDRoundFlatButton(on_release=partial(self.give_answer, right), size_hint=line.size_hint,
                                     pos=line.pos)

        self.add_widget(line)
        self.add_widget(self.btn, index=len(line.children))

    def give_answer(self, right, btn, *args):
        self.disable()
        self.option_grid.change_points(right, btn)

        color = [1, 0, 0, 1]
        if right:
            color = [0, 1, 0, 1]
        duration = random.randrange(1, 2)
        btn.md_bg_color_disabled = "gray"
        anim = Animation(md_bg_color_disabled=[.8, .8, .8, 1], duration=duration) + Animation(
            md_bg_color_disabled=color, duration=.01)
        anim.bind(on_complete=self.option_grid.end_question)
        anim.start(btn)

    def disable(self, *args):
        self.btn.disabled = True


class MainQuestion(MDRelativeLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.options_grid = None

    def new_question(self, question_idx=1, *args):

        # clear old question
        self.clear_widgets()

        # the title
        self.add_widget(
            MDLabel(text=f"Questão {self.app.question_number}", font_style="H3", valign="center", halign="center",
                    size_hint=[1, .2], pos_hint={"center": [.5, .9]}))

        # the question
        question_dict = QUESTIONS[question_idx]
        text = question_dict.get("text", "Nenhum Texto Identificado")

        text_lbl = MDLabel(text=text, padding=(100, 20), pos_hint={"center": [.5, .7]})

        self.add_widget(text_lbl)

        # find the next question

        _options = question_dict.get("options")

        options = list(zip(_options, [True]+[False]*(len(_options)-1)))
        random.shuffle(options)
        self.options_grid = MDGridLayout(cols=1, padding=(100, 40), spacing=[50, 50], size_hint=[1, .5], id="test")

        for letter, [answer, right] in zip("ABCDEFG", options):
            self.options_grid.add_widget(
                Answer(letter=letter, text=f" {answer}", right=right, option_grid=self, size_hint=[1, .2]))
        self.add_widget(self.options_grid)

    def change_points(self, right, _):
        change_points(right)
        self.app.question_number += 1
        self.disable_buttons()

    def disable_buttons(self, *args):
        for line in self.options_grid.children:
            line.disable()

    def end_question(self, *args):
        self.add_widget(MDRectangleFlatButton(text="", size_hint=[1, 1], on_release=partial(self.app.new_question, 1)))

    def do_next_q(self):
        self.app.sm.current = "other"
        self.app.sm.current = "main"
        self.new_question(1)


### Main Window
class MainWindow(MDRelativeLayout):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build()

    def build(self):
        # Title
        self.add_widget(MDLabel(text=f'Trívia de Química!', font_style='H2', size_hint_x=.75, italic=True,
                                pos_hint={'center': [.5, .75]}, halign='center'))

        # ask how many questions
        numbers_grid = MDGridLayout(cols=4, size_hint=[1, .4], pos_hint={'center': [.5, .25]}, padding=[30, 30, 30, 30],
                                    spacing=[0, 50])
        for n in [3, 5]:
            numbers_grid.add_widget(
                MDRectangleFlatButton(text=str(n), font_style='H6',
                                      on_release=partial(self.app.set_number_of_questions, n), size_hint=[1, 1],
                                      text_color='black'))
            numbers_grid.add_widget(Widget())
        for n in [7, 10]:
            numbers_grid.add_widget(Widget())
            numbers_grid.add_widget(
                MDRectangleFlatButton(text=str(n), font_style='H6',
                                      on_release=partial(self.app.set_number_of_questions, n), size_hint=[1, 1],
                                      text_color='black'))
        self.add_widget(numbers_grid)


### Results Window
class ResultsWindow(MDRelativeLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        # self.build()

    def build(self):
        # clear children
        self.clear_widgets()

        # title
        self.add_widget(MDLabel(text=f'Seu Resultado:', font_style='H2', size_hint_x=.75, italic=True,
                                pos_hint={'center': [.5, .75]}, halign='center'))

        # Results
        proportion = TOTAL_POINTS/TOTAL_QUESTIONS
        text = f'Você acertou {TOTAL_POINTS} de {TOTAL_QUESTIONS}!'
        if proportion <= 0:
            text = 'Eita, eita, eita...'
        elif proportion <= .1:
            text = f'Você acertou {TOTAL_POINTS}'
        elif proportion == 1:
            text = f'''Nossa! Você acertou só TUDO!!!
Continue Brilhando!'''

        self.add_widget(
            MDLabel(text=text, font_style='H6', size_hint_x=1,
                    italic=False,
                    pos_hint={'center': [.5, .25]}, halign='center'))

        # Button for going again
        self.add_widget(MDRectangleFlatButton(text = '', on_release = partial(reset_things, self.app), size_hint = [1,1]))


# helpers
def change_points(right):
    global TOTAL_POINTS, TOTAL_QUESTIONS
    TOTAL_POINTS += int(right)
    TOTAL_QUESTIONS += 1

def reset_things(app, *args):
    global TOTAL_POINTS, TOTAL_QUESTIONS
    TOTAL_POINTS = 0
    TOTAL_QUESTIONS = 0
    app.sm.current = 'main'


# MAIN APP
class TriviaQuest(MDApp):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.question_number = 1

        self.question_window = MainQuestion(app=self)

        self.configuration_window = None

        self.main_window = MainWindow(self)

        self.results_window = ResultsWindow(app=self)

        self.questions = []

        self.sm = ScreenManager(transition=Trans(duration=.5))

        self.sm.add_widget(MainScreen(widget=self.main_window, name="main"))
        self.sm.add_widget(MainScreen(widget=self.question_window, name="question"))
        self.sm.add_widget(MainScreen(widget=self.results_window, name="results"))
        self.sm.add_widget(Screen(name="other"))

    def set_number_of_questions(self, number=1, *args):
        self.question_number = 1
        self.questions = random.choices(list(range(len(QUESTIONS))), k=number)
        self.new_question()

    def new_question(self, *args):
        if self.questions:
            self.sm.current = 'other'
            self.question_window.new_question(question_idx=self.questions.pop())
            self.sm.current = 'question'

        else:
            self.sm.current = 'other'
            self.results_window.build()
            self.sm.current = 'results'

    def build(self):
        # self.sm.current = 'main'
        return self.sm


# tests
TriviaQuest().run()

# run
