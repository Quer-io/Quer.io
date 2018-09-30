from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

from service import default_service as ds



class mainWindow():

    def button1(self, value):
        self.lbl.text = self.input.text + '\n'
        self.lbl.text += 'Current query column: ' + str(self.query_column) + '\n'
        self.lbl.text += 'Current reference column: ' + str(self.reference_column)

    def build(self):
        self.layout = BoxLayout(padding=10, orientation="vertical")

        self.reference_column = None
        self.query_column = None

        self.reference_column_spinner = Spinner (
            text="Choose column",
            values=('age', 'income'),
            size_hint=(None,None),
            size=(125,42)
        )

        self.query_column_spinner = Spinner (
            text="Choose column",
            values=('age', 'income'),
            size_hint=(None,None),
            size=(125,42)
        )

        self.reference_column_spinner.bind(text=self.select_reference_column)
        self.query_column_spinner.bind(text=self.select_query_column)

        self.layout.add_widget(self.query_column_spinner)
        self.layout.add_widget(self.reference_column_spinner)              
        self.lbl = Label(text='Welcome to Querio')
        self.layout.add_widget(self.lbl)
        self.btn1 = Button(text='This is a button')
        self.btn1.bind(on_press=self.button1)
        self.layout.add_widget(self.btn1)
        self.input = TextInput(id='txt', text='Insert Value')
        self.layout.add_widget(self.input)

        return self.layout




    def select_reference_column(self, spinner, text):
        self.reference_column = text
    
    def select_query_column(self, spinner, text):
        self.query_column = text




