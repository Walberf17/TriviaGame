"""
A easy way to insert questions
for now only words, no images
"""

# import kivy
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton, MDRectangleFlatButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.gridlayout import MDGridLayout

# import other things
import json
from os.path import join
import re

# variables
QUESTIONS = []


# helpers
def subscrite(arg):
    if arg.span()[0] == 0:
        return arg[0]
    else:
        return f'[sub]{arg[0]}[/sub]'


def load_file():
    global QUESTIONS
    with open(join('..', 'questions.json'), 'r') as f:
        QUESTIONS = json.load(f)


def save_file():
    with open(join('..', 'questions.json'), 'w') as f:
        json.dump(QUESTIONS, f, indent=4, ensure_ascii=False)

load_file()
print(len(QUESTIONS))
# main window
class MainWindow(MDRelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self, *args):
        self.add_widget(MDLabel(text='Criar Questões', size_hint=[1, .2], pos_hint={'center': [.5, .9]},
                                halign='center', font_style='H2'))
        self.question = MDTextField(hint_text='Pergunta', size_hint=[.7, .2], padding=[50, 50, 50, 50], required = True,
                                    pos_hint={'center': [.5, .7]}, multiline=True, mode='round', line_anim=True,
                                    helper_text_color_normal="black",text_color_normal = [0,0,0,1],text_color_focus=[0,0,0,1],
                                    helper_text='Digite aqui sua pergunta', helper_text_mode='on_focus')
        self.add_widget(self.question)
        self.options = []
        self.answer = MDTextField(hint_text='Resposta', size_hint=[.9, .2], padding=[50, 50, 50, 50], required = True,
                                  pos_hint={'center': [.5, .7]}, multiline=False, mode='round', line_anim=True,
                                  helper_text_color_normal="black",text_color_normal = [0,0,0,1],text_color_focus=[0,0,0,1],
                                  helper_text='Digite a resposta para a pergunta', helper_text_mode='on_focus',
                                  on_text_validate = self.add_option)
        self.options_grid = MDGridLayout(cols = 1, size_hint = [1,.5], pos_hint={'center':[.5,.25]}, spacing = 20, padding = [30,20,30,20])
        self.options_grid.add_widget(self.answer)
        new_line_save = MDGridLayout(cols = 2, size_hint = [.9,.2], pos_hint = {'center':[.5 , .05]},adaptive_size = True)
        new_line_save.add_widget(MDRoundFlatButton(text='Adicionar opção',on_release=self.add_option))
        new_line_save.add_widget(MDRoundFlatButton(text='salvar',on_release=self.get_options))
        self.add_widget(new_line_save)
        self.add_widget(self.options_grid)

    def add_option(self, *args):
        option = MDTextField(hint_text='Resposta', size_hint=[.9, .2], padding=[50, 50, 50, 50],
                             pos_hint={'center': [.5, .7]}, multiline=False, mode='round', line_anim=True,
                             helper_text_color_normal="black",text_color_normal = [0,0,0,1],text_color_focus=[0,0,0,1],
                             helper_text='Digite a resposta para a pergunta', helper_text_mode='on_focus',
                             on_text_validate = self.add_option)
        self.options_grid.add_widget(option)
        option.focus = True

    def subscrite_text(self, text):
        return re.sub('(?<=\D)(?<=\S)(?<=[^xX"])[0-9]+', subscrite, text)

    def validate_fields(self, field):
        # field.text = self.subscrite_text(field.text)
        self.add_option()

    def new_question(self):
        self.clear_widgets()
        self.build()

    def get_options(self, *args):
        answers = list()
        if self.answer.text == '' or self.question.text == '':
            print('não salvei')
            return
        for line in self.options_grid.children[::-1]:
            if isinstance(line, MDTextField):
                answers.append(self.subscrite_text(line.text))
        question = {
            "text" : self.subscrite_text(self.question.text),
            "options": answers
        }
        QUESTIONS.append(question)
        save_file()
        print('Pergunta Salva')
        self.new_question()



# main app
class MyApp(MDApp):
    def build(self):
        return MainWindow()


MyApp().run()
