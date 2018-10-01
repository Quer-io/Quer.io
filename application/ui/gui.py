from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle
from service.database_and_model_service import DatabaseAndModelService as ds


class mainWindow(GridLayout):

    def button1(self, value):
        self.lbl.text = 'Value given: ' + self.input.text + '\n'
        self.lbl.text += 'Current query column: ' + str(self.query_column) + '\n'
        self.lbl.text += 'Current reference column: ' + str(self.reference_column + '\n')
        result = self.age_model.get_user_defined_query('avg', str(self.reference_column), str(self.query_column), self.input.text)
        if type(result) is not None:
            self.lbl.text += 'Result: ' + str(result)
        else:
            self.lbl.text += 'Error in database'
        if str(self.reference_column) is 'age':
            self.lbl.text += ' \n Prediction: %d, Variance: %d' % self.age_model.get_prediction_for_value(self.input.text)
        else:
            self.lbl.text += 'Prediction: %d, Variance: %d' % self.income_model.get_prediction_for_value(self.input.text)

    def build(self):
        self.income_model = ds('income', 'age')
        self.age_model = ds('age', 'income')
        self.layout = GridLayout(cols=2)

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

        self.lbl = Label(text='Welcome to Querio')
        self.exmpl = Label(text_size=(self.lbl.width, self.lbl.height),
                           height=self.lbl.texture_size[1],
                           halign="left",
                           valign="top",
                           text=str(self.income_model.get_example_from_db()))
        self.btn1 = Button(text='This is a button')
        self.btn1.bind(on_press=self.button1)
        self.input = TextInput(text='Insert Value', multiline=False)

        self.spinner_layout = GridLayout(cols=2)
        self.spinner_layout.add_widget(self.query_column_spinner)
        self.spinner_layout.add_widget(self.reference_column_spinner)

        self.layout.add_widget(self.spinner_layout)
        self.layout.add_widget(self.input)
        self.layout.add_widget(self.exmpl)
        self.layout.add_widget(self.btn1)
        self.layout.add_widget(self.lbl)

        return self.layout

    def select_reference_column(self, spinner, text):
        self.reference_column = text

    def select_query_column(self, spinner, text):
        self.query_column = text
