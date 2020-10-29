from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
import kivy.utils
#from MyFirebase import MyFirebase
import requests
import json
import webbrowser
"""from plyer import notification
from plyer.compat import PY2
from os.path import join, dirname, realpath"""
#pruebas git

class HomeScreen(Screen):
    pass

class Login(Screen):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

GUI = Builder.load_file("kv/main.kv", encoding="utf-8")

class MainApp(App):
    def build(self):
        # self.my_firebase = MyFirebase()
        # Clock.schedule_interval(self.Callback_Clock, 30)
        return GUI

    def on_start(self):
        self.change_screen("home_screen")

    def change_screen(self, screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name

if __name__ == "__main__":
    MainApp().run()