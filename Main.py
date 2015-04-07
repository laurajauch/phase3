import kivy
kivy.require('1.0.7')


from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp

class testApp(App):
    pass


dropdown = DropDown()
for index in range(2):
    btn = Button(text = 'Stokes', size_hint_y = None, height = 44)
    btn.bind(on_release = lambda btn: dropdown.select(btn.text))
    dropdown.add_widget(btn)

mainbutton = Button(text='type', size_hint= (None, None))
mainbutton.bind(on_release = dropdown.open)
runTouchApp(mainbutton)


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
    #testApp().run()

