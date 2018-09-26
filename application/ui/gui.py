from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


def mainWindow():
    layout = BoxLayout(padding=10)
    layout.add_widget(Label(text='Welcome to Querio'))
    btn1 = Button(text='This is a button')
    btn1.bind(on_press=button1)
    layout.add_widget(btn1)
    return layout


def button1(instance):
    print('button')
