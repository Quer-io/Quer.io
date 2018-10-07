from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox


TEXT_VALUE = 'text'

class DBWindow():
    def __init__(self):
        self.db_connection = (True, '')
        self.use_config_file = False

        self.layout = GridLayout(cols=2)

        self.create_config_file_layout()
        self.create_close_button_layout()
        self.create_username_box()
        self.create_password_box()
        self.create_host_box()
        self.create_port_box()
        self.create_db_name_box()
        self.create_info_box()
        self.create_save_button_box()

    def create_close_button_layout(self):
        self.close_button_layout = AnchorLayout(
            anchor_x='right', anchor_y='top'
        )
        self.close_button = Button(text='Close', size_hint=(None, None), height=25)
        self.close_button_layout.add_widget(self.close_button)
        self.layout.add_widget(self.close_button_layout)

    def create_username_box(self):
        self.username_label = Label(text="Username")
        self.username_input = TextInput(write_tab=False)
        self.username_input.bind(focus=self.clear_info_label)
        self.layout.add_widget(self.username_label)
        self.layout.add_widget(self.username_input)

    def create_password_box(self):
        self.password_label = Label(text="Password")
        self.password_input = TextInput(password=True, write_tab=False)
        self.password_input.bind(focus=self.clear_info_label)
        self.layout.add_widget(self.password_label)
        self.layout.add_widget(self.password_input)

    def create_host_box(self):
        self.host_label = Label(text="Host")
        self.host_input = TextInput(write_tab=False)
        self.host_input.bind(focus=self.clear_info_label)
        self.layout.add_widget(self.host_label)
        self.layout.add_widget(self.host_input)

    def create_port_box(self):
        self.port_label = Label(text="Port")
        self.port_input = TextInput(write_tab=False)
        self.port_input.bind(focus=self.clear_info_label)
        self.layout.add_widget(self.port_label)
        self.layout.add_widget(self.port_input)

    def create_db_name_box(self):
        self.db_name_label = Label(text="Database name")
        self.db_name_input = TextInput(write_tab=False)
        self.db_name_input.bind(focus=self.clear_info_label)
        self.layout.add_widget(self.db_name_label)
        self.layout.add_widget(self.db_name_input)

    def create_info_box(self):
        self.info_label = Label()
        self.layout.add_widget(self.info_label)

    def create_save_button_box(self):
        self.save_button = Button(text='Save')
        self.save_button.bind(on_press=self.save_database_connection)
        self.layout.add_widget(self.save_button)

    def on_checkbox_active(self, checkbox, value):
        if value:
            self.use_config_file = True
        else:
            self.use_config_file = False

    def create_config_file_layout(self):
        self.config_file_layout = BoxLayout(padding=10, orientation='horizontal')
        self.config_label = Label(font_size=11, text='Use configuration.ini')
        self.config_file_checkbox = CheckBox()
        self.config_file_checkbox.bind(active=self.on_checkbox_active)

        self.config_file_layout.add_widget(self.config_label)
        self.config_file_layout.add_widget(self.config_file_checkbox)

        self.layout.add_widget(self.config_file_layout)

    def clear_info_label(self, instance, value):
        setattr(self.info_label, TEXT_VALUE, '')

    def save_database_connection(self, value):
        try:
            port = int(self.port_input.text.strip())
        except ValueError:
            setattr(self.info_label, TEXT_VALUE, 'Port has to be a number')
            return

        connection = "postgresql://" + self.username_input.text.strip() + ":" + self.password_input.text.strip()
        connection += "@" + self.host_input.text.strip() + ":" + self.port_input.text.strip() + "/" + self.db_name_input.text.strip()
        self.db_connection = (self.use_config_file, connection)
        setattr(self.info_label, TEXT_VALUE, 'Saved!')    

