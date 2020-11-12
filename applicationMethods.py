from kivymd.app import MDApp
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior
from kivymd.theming import ThemableBehavior, ThemeManager
from kivymd.uix.list import OneLineIconListItem, MDList
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from functools import partial
import requests
import json

class ContentNavigationDrawer(BoxLayout):
    pass

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""
        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color
    
class MyTextInput(TextInput):
    pass

class SmoothButton(Button):
    pass

class MyLabel(Label):
    pass

class MyCheckBox(CheckBox):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class ApplicationMethods():

    def __init__(self, data_base):
        self.data_base = data_base

    def add_ingre(self, app):
        scroll = app.root.ids['new_ingre'].ids['l_recipe']
        text=MyTextInput(hint_text='Ingrediente')
        scroll.add_widget(text)
    
    def change_screen(self, app, screen_name):
        screen_manager = app.root.ids['screen_manager']
        # screen_manager.transition=FadeTransition()
        screen_manager.current = screen_name
        if screen_name == 'submit':
            app.root.ids['submit'].ids['title'].text = app.root.ids['new_ingre'].ids['titulo'].text
        if screen_name == 'new_ingre':
            app.root.ids['new_ingre'].ids['l_recipe'].clear_widgets()

    def cook(self, app, data):
        self.change_screen(app, 'cooking')
        scroll = app.root.ids['cooking'].ids['receta_id']
        scroll.text=data

    def getText(self, app):
        scroll = app.root.ids['new_ingre'].ids['l_recipe']
        child=''
        for children in scroll.children:
            child+=children.text+';'
        datos = {app.root.ids['new_ingre'].ids['titulo'].text: {'ingredientes': child[:-1], 'preparacion': app.root.ids['submit'].ids['cooking_input'].text}}
        self.data_base.patch(json.dumps(datos), self.category)
        app.on_start()
        # self.ping(self.category, app.root.ids['new_ingre'].ids['titulo'].text)

    def listado(self, app, option):
        self.category=option
        self.change_screen(app, 'recipes')
        scroll = app.root.ids['recipes'].ids['l_recipe']
        data = app.data[option]
        scroll.clear_widgets()
        for key in data:
            btn=SmoothButton(text='[color=#000000]'+str(key)+'[/color]',
                on_release=partial(self.receta, app=app, data=data[key]))
            scroll.add_widget(btn)

    def receta(self, caller, app, data):
        self.change_screen(app, 'ingredients')
        scroll = app.root.ids['ingredients'].ids['l_recipe']
        scroll.clear_widgets()
        dat=data['ingredientes'].split(";")
        for i in dat:
            etiq=MyLabel(text=str(i),color= (0,0,0,1))
            scroll.add_widget(etiq)
            scroll.add_widget(MyCheckBox(size_hint_x=None, width=100))
        button_next = app.root.ids['ingredients'].ids['next']
        button_next.on_release = partial(self.cook, app=app, data=data['preparacion'])

    def icons(self, app):
        icons_item = {
            "notebook-edit": "Editar receta",
            "notebook-remove": "Eliminar receta",
            "notebook-plus": "A\u00F1adir Receta",
        }
        list_recipes = app.root.ids['list_recipes'].ids['content_drawer'].ids['md_list']
        recipes = app.root.ids['recipes'].ids['content_drawer'].ids['md_list']
        ingredients = app.root.ids['ingredients'].ids['content_drawer'].ids['md_list']
        cooking = app.root.ids['cooking'].ids['content_drawer'].ids['md_list']
        list_recipes.clear_widgets(); recipes.clear_widgets();ingredients.clear_widgets();cooking.clear_widgets()
        for icon_name in icons_item.keys():
            list_recipes.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name], on_release=partial(self.icons_drawers_effects, option=icon_name,app=app))
            )
            recipes.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name], on_release=partial(self.icons_drawers_effects, option=icon_name,app=app))
            )
            ingredients.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name], on_release=partial(self.icons_drawers_effects, option=icon_name,app=app))
            )
            cooking.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name], on_release=partial(self.icons_drawers_effects, option=icon_name,app=app))
            )
    
    def icons_drawers_effects(self, caller, option, app):
        if option == 'notebook-edit':
            pass
        elif option == 'notebook-remove':
            pass
        else:
            pass

    # para relizar el delete de la recipe
    # def ping(self, category, title):
    #     self.data_base.delete(category, title)


class Login(Screen):
    pass

class ListRecipes(Screen):
    pass

class Recipes(Screen):
    pass

class Ingredients(Screen):
    pass

class Cooking(Screen):
    pass

class Test(Screen):
    pass

class New_ingre(Screen):
    pass

class Submit(Screen):
    pass
    