import kivy
from kivy.app import App
import sys
from ui import interface, gui
kivy.require('1.10.1')

class userInterfaceApp(App):
    def build(self):
        return gui.mainWindow().build()


def main():
    interface.baseUi()


def run_test():
    # TODO: test some runtime functionality here
    print('App started successfully')


if __name__ == '__main__':
    if(len(sys.argv) > 1 and sys.argv[1] == '--run-test'):
        run_test()
    else:
        userInterfaceApp().run()
        main()
