from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
# from kivy.animation import Animation
# from kivy.core.window import Window
from manageDatabase import manageDatabase
from applicationMethods import ApplicationMethods
import requests
import json
"""from plyer import notification
from plyer.compat import PY2
from os.path import join, dirname, realpath"""

GUI = Builder.load_file("kv/main.kv", encoding="utf-8")

class MainApp(App):
    # def __init__(self, **kwargs):
    #     super(MainApp, self).__init__(**kwargs)
    #     Window.bind(on_keyboard=self.on_key)
        
    def build(self):
        self.database = manageDatabase()
        self.application = ApplicationMethods(self.database)
        # Clock.schedule_interval(self.breath, 1)
        return GUI

    def on_start(self):
        # self.change_screen("login")
        self.data = self.database.get()
        self.application.change_screen(self,"list_recipes")
    


    # def on_key(self, window, key, *args):
    #     if key == 27:  # the esc key
    #         self.change_screen('home_screen')

    # def breath(self, dtx):
    #     anim = Animation(size_hint=(.15,.05), t= 'in_quad', duration= .5) + Animation(size=(.2,.1), t= 'in_quad', duration= .5)
    #     tgt=self.root.ids['recipes'].ids['add']
    #     anim.start(tgt)


if __name__ == "__main__":
    MainApp().run()