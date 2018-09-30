from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class mainWindow():

    def button1(self, value):
        self.lbl.text = self.input.text

    def build(self):
        self.layout = BoxLayout(padding=10)
        self.lbl = Label(text='Welcome to Querio')
        self.layout.add_widget(self.lbl)
        self.btn1 = Button(text='This is a button')
        self.btn1.bind(on_press=self.button1)
        self.layout.add_widget(self.btn1)
        self.input = TextInput(id='txt', text='Insert Value')
        self.layout.add_widget(self.input)
        return self.layout
