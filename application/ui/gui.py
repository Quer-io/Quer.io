from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle
from service import default_service as ds


class mainWindow(BoxLayout):

    def button1(self, value):
        self.lbl.text = self.input.text + '\n'
        self.lbl.text += 'Current query column: ' + str(self.query_column) + '\n'
        self.lbl.text += 'Current reference column: ' + str(self.reference_column + '\n')
        self.lbl.text += 'Result: ' + str(ds.get_user_defined_query('avg', str(self.reference_column), str(self.query_column), self.input.text))

    def build(self):
        self.layout = BoxLayout(padding=10, orientation="vertical")

        self.reference_column = None
        self.query_column = None

        self.reference_column_spinner = Spinner(
            text="Choose column",
            values=('age', 'income'),
            size_hint=(None, None),
            size=(125, 42)
        )

        self.query_column_spinner = Spinner(
            text="Choose column",
            values=('age', 'income'),
            size_hint=(None, None),
            size=(125, 42)
        )

        self.reference_column_spinner.bind(text=self.select_reference_column)
        self.query_column_spinner.bind(text=self.select_query_column)

        self.layout.add_widget(self.query_column_spinner)
        self.layout.add_widget(self.reference_column_spinner)
        self.lbl = Label(text='Welcome to Querio')
        self.exmpl = Label(text_size=(self.lbl.width, self.lbl.height),
                           height=self.lbl.texture_size[1],
                           halign="left",
                           valign="top",
                           text=str(ds.get_example_from_db()))
        self.btn1 = Button(text='This is a button')
        self.btn1.bind(on_press=self.button1)
        self.input = TextInput(id='txt', text='Insert Value', multiline=False)
        self.layout.add_widget(self.input)
        self.layout.add_widget(self.exmpl)
        self.layout.add_widget(self.btn1)
        self.layout.add_widget(self.lbl)
        return self.layout

    def select_reference_column(self, spinner, text):
        self.reference_column = text

    def select_query_column(self, spinner, text):
        self.query_column = text
