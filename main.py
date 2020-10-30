from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.button import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.checkbox import CheckBox
from functools import partial
import kivy.utils
#from MyFirebase import MyFirebase
import requests
import json
import webbrowser
"""from plyer import notification
from plyer.compat import PY2
from os.path import join, dirname, realpath"""
#pruebas gi

class HomeScreen(Screen):
    pass

class Login(Screen):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class WrapButton(Button):
    pass

class ListRecipes(Screen):
    pass

class Recipes(Screen):
    pass

class Ingredients(Screen):
    pass

class MyLabel(Label):
    pass

GUI = Builder.load_file("kv/main.kv", encoding="utf-8")

class MainApp(App):
    def build(self):
        # self.my_firebase = MyFirebase()
        # Clock.schedule_interval(self.Callback_Clock, 30)
        return GUI

    def on_start(self):
        result = requests.get("https://recetas-acfc9.firebaseio.com/1.json")
        self.data = json.loads(result.content.decode())
        print(self.data)
        # self.change_screen("home_screen")
        self.change_screen("list_recipes")
        recipe_text=self.root.ids['home_screen'].ids['receta_id']
        recipe_text.text="La lechuga se echa por la alcantarilla para despues aaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaa servirla con perejil potado, salteado en una sarten con media mierdaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    def change_screen(self, screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name
    
    def ping(self, n, value):
        print("funciona")
    

    def listado(self, option):
        self.change_screen('recipes')
        scroll = self.root.ids['recipes'].ids['l_recipe']
        data = self.data[option]
        for key in data:
            btn=Button(text=str(key), on_press=partial(self.receta, data=data[key]))
            scroll.add_widget(btn)

    def receta(self, caller, data):
        self.change_screen('ingredients')
        scroll = self.root.ids['ingredients'].ids['l_recipe']
        dat=data['ingredientes'].split(", ")
        scroll.add_widget(Image(source="icons/ingredients.png"))
        scroll.add_widget(Image(source="icons/ingredients.png"))
        for i in dat:
            etiq=MyLabel(text=str(i))
            scroll.add_widget(etiq)
            scroll.add_widget(CheckBox())



if __name__ == "__main__":
    MainApp().run()