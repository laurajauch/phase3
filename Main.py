import kivy
kivy.require('1.0.7')


from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp

class testApp(App):
    #Design elements are containted in the test.kv file which is kivy looks for when the program starts.
    pass



if __name__ == '__main__':
    testApp().run()

