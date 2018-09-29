import kivy
from ui import interface, gui
from kivy.app import App
kivy.require('1.10.1')


class userInterfaceApp(App):
    def build(self):
        return gui.mainWindow().build()


def main():
    interface.baseUi()


if __name__ == '__main__':
    userInterfaceApp().run()
    main()
