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
    dropdown = DropDown()
    for index in range(2):
        btn = Button(text = 'Stokes', size_hint_y = None, height = 44)
        btn.bind(on_release = lambda btn: dropdown.select(btn.text))
        dropdown.add_widget(btn)

    mainbutton = Button(text='type', size_hint= (None, None))
    mainbutton.bind(on_release = dropdown.open)
    runTouchApp(mainbutton)

    dropdown1 = DropDown()
    for index in range(2):
        btn1 = Button(text = 'Steady State',size_hint_y = None, height = 44)
        btn1.bind(on_release = lambda btn1: dropdown1.select(btn1.text))
        dropdown.add_widget(btn1)

    nextbutton = Button(text='state', size_hint= (None, None), height = 44)
    nextbutton.bind(on_release = dropdown1.open)
    runTouchApp(nextbutton)

    dropdown2 = DropDown()
    for index in range(2):
        btn2 = Button(text = 'h-auto',size_hint_y = None, height = 44)
        btn2.bind(on_release = lambda btn2: dropdown2.select(btn2.text))
        dropdown.add_widget(btn2)

    nextbutton1 = Button(text='Refine', size_hint= (None, None), height = 44)
    nextbutton1.bind(on_release = dropdown2.open)
    runTouchApp(nextbutton1)

    dropdown3 = DropDown()
    for index in range(5):
        btn3 = Button(text = 'Mesh',size_hint_y = None, height = 44)
        btn3.bind(on_release = lambda btn3: dropdown3.select(btn3.text))
        dropdown.add_widget(btn3)

    nextbutton2 = Button(text='Refine', size_hint= (None, None), height = 44)
    nextbutton2.bind(on_release = dropdown3.open)
    runTouchApp(nextbutton2)
