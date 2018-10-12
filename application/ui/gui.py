from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from service.database_and_model_service import DatabaseAndModelService as ds
from ui.database_config_window import DBWindow


class mainWindow(GridLayout):

    def button1(self, value):
        print(self.db_conf.db_connection)
        self.lbl.text = 'Value given: ' + self.input.text + '\n'
        self.lbl.text += 'Current query column: ' + str(self.query_column) + '\n'
        self.lbl.text += 'Current reference column: ' + str(self.reference_column + '\n')
        result = self.age_model.get_user_defined_query('avg', str(self.reference_column), str(self.query_column), self.input.text)
        if type(result) is not None:
            self.lbl.text += 'Result: ' + str(result) + '\n'
        else:
            self.lbl.text += 'Error in database \n'
        if str(self.reference_column) is 'age':
            self.lbl.text += str(self.age_model.get_prediction_for_value(self.input.text))
        else:
            self.lbl.text += str(self.income_model.get_prediction_for_value(self.input.text))

    def button2(self, value):
        self.db_popup.open()

    def button3(self, value):
        self.ex_popup.open()

    def connect(self):
        self.income_model = ds('income', 'age', self.db_conf.db_connection)
        self.age_model = ds('age', 'income', self.db_conf.db_connection)

    def connect_button(self, value):
        self.connect()

        if self.age_model.db.connected:
            self.db_info_label.text = 'Connection succesful!'
            self.btn1.disabled = False
        else:
            self.db_info_label.text = 'Error with connection. Check your database settings'
            self.btn1.disabled = True

    def build(self):

        self.db_conf = DBWindow()

        self.connect()

        self.ex_conf = ExampleWindow(self.age_model)

        self.layout = GridLayout(cols=2)
        self.reference_column = None
        self.query_column = None

        self.db_popup = Popup(title="Database configuration",
                              content=self.db_conf.layout,
                              size_hint=(None, None), size=(400, 400))
        self.db_conf.close_button.bind(on_press=self.db_popup.dismiss)

        self.ex_popup = Popup(title="Example data",
                              content=self.ex_conf.layout,
                              size_hint=(None, None), size=(400, 400))
        self.ex_conf.close_button.bind(on_press=self.ex_popup.dismiss)

        self.reference_column_spinner = Spinner(
            text="Choose column",
            values=self.age_model.get_column_names_from_db(),
            size_hint=(None, None),
            size=(125, 42)
        )

        self.query_column_spinner = Spinner(
            text="Choose column",
            values=self.age_model.get_column_names_from_db(),
            size_hint=(None, None),
            size=(125, 42)
        )

        self.reference_column_spinner.bind(text=self.select_reference_column)
        self.query_column_spinner.bind(text=self.select_query_column)

        self.lbl = Label(text='Welcome to Querio')
        self.exmpl = Button(text="View Example")
        self.exmpl.bind(on_press=self.button3)

        self.btn1 = Button(text='This is a button')
        self.btn1.bind(on_press=self.button1)

        self.input = TextInput(text='Insert Value', multiline=False)

        self.spinner_layout = GridLayout(cols=2)
        self.spinner_layout.add_widget(self.query_column_spinner)
        self.spinner_layout.add_widget(self.reference_column_spinner)
        self.layout.add_widget(self.exmpl)
        self.layout.add_widget(self.create_db_layout())
        self.layout.add_widget(self.spinner_layout)
        self.layout.add_widget(self.input)
        self.layout.add_widget(self.lbl)
        self.layout.add_widget(self.btn1)

        return self.layout

    def select_reference_column(self, spinner, text):
        self.reference_column = text

    def select_query_column(self, spinner, text):
        self.query_column = text

    def create_db_layout(self):
        self.db_layout = BoxLayout(orientation='vertical')
        self.btn2 = Button(text='Database config')
        self.btn2.bind(on_press=self.button2)

        self.db_info_label = Label()

        self.connect_btn = Button(text='Connect')
        self.connect_btn.bind(on_press=self.connect_button)

        self.db_layout.add_widget(self.btn2)
        self.db_layout.add_widget(self.connect_btn)
        self.db_layout.add_widget(self.db_info_label)

        return self.db_layout


class ExampleWindow():
    def __init__(self, ds):

        self.layout = GridLayout(cols=2)
        examples = ds.get_example_from_db()
        self.layout.add_widget(Label())
        self.create_close_button_layout()

        for x, y in sorted(examples):
            self.createLabel(x, y)

    def create_close_button_layout(self):
        self.close_button_layout = AnchorLayout(
            anchor_x='right', anchor_y='top'
        )
        self.close_button = Button(text='Close', size_hint=(None, None), height=25)
        self.close_button_layout.add_widget(self.close_button)
        self.layout.add_widget(self.close_button_layout)

    def createLabel(self, x, y):
        self.layout.add_widget(Label(
                                    halign="left",
                                    valign="top",
                                    text=str(x)))
        self.layout.add_widget(Label(
                                    halign="left",
                                    valign="top",
                                    text=str(y)))
