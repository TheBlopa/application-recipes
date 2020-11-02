from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.button import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from functools import partial
# from kivy.core.window import Window
import kivy.utils
#from MyFirebase import MyFirebase
import requests
import json
# import webbrowser
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

class SmoothButton(Button):
    pass

class ListRecipes(Screen):
    pass

class Recipes(Screen):
    pass

class Ingredients(Screen):
    pass

class Cooking(Screen):
    pass

class MyLabel(Label):
    pass

class MyCheckBox(CheckBox):
    pass

class MyTextInput(TextInput):
    pass

class Test(Screen):
    pass

class New_ingre(Screen):
    pass

class Submit(Screen):
    pass

GUI = Builder.load_file("kv/main.kv", encoding="utf-8")

class MainApp(App):
    # def __init__(self, **kwargs):
    #     super(MainApp, self).__init__(**kwargs)
    #     Window.bind(on_keyboard=self.on_key)
        
    def build(self):
        # self.my_firebase = MyFirebase()
        # Clock.schedule_interval(self.Callback_Clock, 30)
        return GUI

    def on_start(self):
        # self.change_screen("test")
        result = requests.get("https://recetas-acfc9.firebaseio.com/1.json")
        self.data = json.loads(result.content.decode())
        self.change_screen("list_recipes")

    def change_screen(self, screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name
        if screen_name == 'submit':
            self.root.ids['submit'].ids['title'].text = self.root.ids['new_ingre'].ids['titulo'].text

    
    def add_ingre(self):
        scroll = self.root.ids['new_ingre'].ids['l_recipe']
        text=MyTextInput(text='Ingrediente')
        scroll.add_widget(text)

    def getText(self):
        scroll = self.root.ids['new_ingre'].ids['l_recipe']
        child=''
        for children in scroll.children:
            child+=children.text+';'
        datos = {self.root.ids['new_ingre'].ids['titulo'].text: {'ingredientes': child[:-1], 'preparacion': self.root.ids['submit'].ids['cooking_input'].text}}
        requests.post("https://recetas-acfc9.firebaseio.com/1/%s.json"% (self.category), data=json.dumps(datos))
        self.on_start()
    

    def listado(self, option):
        self.category=option
        self.change_screen('recipes')
        scroll = self.root.ids['recipes'].ids['l_recipe']
        head = self.root.ids['recipes'].ids['recipes_image']
        data = self.data[option]
        head.clear_widgets()
        scroll.clear_widgets()
        head.add_widget(Image(source="icons/recipe.png"))
        for key in data:
            for title in data[key].keys():
                btn=SmoothButton(text='[color=#000000]'+str(title)+'[/color]', 
                    on_release=partial(self.receta, data=data[key][title]))
                scroll.add_widget(btn)

    def receta(self, caller, data):
        self.change_screen('ingredients')
        scroll = self.root.ids['ingredients'].ids['l_recipe']
        scroll.clear_widgets()
        dat=data['ingredientes'].split(";")
        for i in dat:
            etiq=MyLabel(text=str(i),color= (0,0,0,1))
            scroll.add_widget(etiq)
            scroll.add_widget(MyCheckBox(size_hint_x=None, width=100))
        button_next = self.root.ids['ingredients'].ids['next']
        button_next.on_release = partial(self.cook, data=data['preparacion'])
    
    def cook(self, data):
        self.change_screen('cooking')
        scroll = self.root.ids['cooking'].ids['receta_id']
        scroll.text=data

    # def on_key(self, window, key, *args):
    #     if key == 27:  # the esc key
    #         self.change_screen('home_screen')


if __name__ == "__main__":
    MainApp().run()