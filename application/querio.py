from ui import interface, gui
from kivy.app import App


class userInterface(App):
    def build(self):
        return gui.mainWindow()


def main():
    interface.baseUi()


if __name__ == '__main__':
    userInterface().run()
    main()
