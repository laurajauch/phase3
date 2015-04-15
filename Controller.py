import kivy
kivy.require('1.0.7')
from kivy.app import App

"""
Controller

The driver for the PyCamellia GUI. Main also assumes the
responsibility of reading and writing to the view (test.kv).
"""
class Controller(self):



"""
Design elements are contained in the test.kv file
which kivy will look in when the program starts as
a result of this empty class.
"""
class testApp(App):
    pass



if __name__ == '__main__':
    testApp().run()

