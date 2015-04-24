from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

class MyLayoutApp(App):
    def build(self):
        layout = FloatLayout(size = (300,300))
        button = Button(
            text = 'foo',
            size_hint=(.6 , .6),
            pos_hint={'x':.2,'y':2})
        layout.add_widget(button)

        return layout
    

if __name__ == '__main__':
    MyLayoutApp().run()
