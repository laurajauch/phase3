import kivy
kivy.require('1.0.7')
from kivy.app import App
from Model import *

"""
Controller

The driver for the PyCamellia GUI. Main also assumes the
responsibility of reading and writing to the view (test.kv).
"""
class Controller(object):
    def run(self):
        self.model = Model()
        testApp().run()
    

"""
Design elements are contained in the test.kv file
which kivy will look in when the program starts as
a result of this empty class.
"""
class testApp(App):
    pass



if __name__ == '__main__':
    controller = Controller()
    controller.run()

