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
        # Called when tap on a menu item.
        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color
  

class ApplicationMethods():

    def __init__(self, data_base):
        """Init the class define the database to use"""
        self.data_base = data_base

    def change_screen(self, app, screen_name):
        """Change the screen with screen_manager in kv file

        Parameter
        ---------
        app : root app
        screen_name: str 
        """
        screen_manager = app.root.ids['screen_manager']
        screen_manager.current = screen_name
        # Put title of the new recipe in a label in the last screen of add a recipe
        if screen_name == 'submit':
            app.root.ids['submit'].ids['title'].text = app.root.ids['new_ingre'].ids['titulo'].text
        # Clear all textinput that write ingredientes when the app change to this screen 
        if screen_name == 'new_ingre':
            app.root.ids['new_ingre'].ids['l_recipe'].clear_widgets()

    def add_ingre(self, app):
        """Add new TextInput to new_ingre screen, only aviable for add or edit a recipe

        Parameters
        ----------
        app: root app
        """
        scroll = app.root.ids['new_ingre'].ids['l_recipe']
        text=MyTextInput(hint_text='Ingrediente')
        scroll.add_widget(text)
    
    def cook(self, app, data):
        """Show the information of how to cook a recipe on his label in cooking screen
        Parameters
        ----------
        app: root app
        data: str
        """
        self.change_screen(app, 'cooking')
        scroll = app.root.ids['cooking'].ids['receta_id']
        scroll.text=data

    def getText(self, app):
        """Collect data to patch in the database to add or edit a recipe
        Parameters
        ----------
        app: root app
        """
        scroll = app.root.ids['new_ingre'].ids['l_recipe']
        child=''
        # Transform the data from ingredientes with seperation to later shown them separately
        for children in scroll.children:
            child+=children.text+';'
        # Complete the data for the recipe with all and call path from database
        datos = {app.root.ids['new_ingre'].ids['titulo'].text: {'ingredientes': child[:-1], 'preparacion': app.root.ids['submit'].ids['cooking_input'].text}}
        self.data_base.patch(json.dumps(datos), self.category)
        # Reinitialize the app
        app.on_start()

    def listado(self, app, option, edit_delete):
        """Show a list of buttons of the recipes from the option chosen
        Parameters
        ----------
        app: root app
        option: str
        edit-_delete: str"""
        self.category=option
        self.change_screen(app, 'recipes')
        scroll = app.root.ids['recipes'].ids['l_recipe']
        data = app.data[option]
        scroll.clear_widgets()
        # Set the funtion of the buttons if the comand is delete or edit or only view
        for key in data:
            if edit_delete == 'delete':
                btn=SmoothButton(text='[color=#000000]'+str(key)+'[/color]',
                    on_release=partial(self.delete, category=self.category, title=key, app=app))
            elif edit_delete == 'edit':
                btn=SmoothButton(text='[color=#000000]'+str(key)+'[/color]',
                    on_release=partial(self.edit, app=app, title=key, data=data[key]))
            else:
                btn=SmoothButton(text='[color=#000000]'+str(key)+'[/color]',
                    on_release=partial(self.receta, app=app, data=data[key]))                
            scroll.add_widget(btn)

    def receta(self, caller, app, data):
        """Show a list of ingredients for the chosen recipe
        Parameter
        ---------
        caller: require parameter of partial
        app: root app
        data: list of str
        """
        self.change_screen(app, 'ingredients')
        scroll = app.root.ids['ingredients'].ids['l_recipe']
        scroll.clear_widgets()
        dat=data['ingredientes'].split(";")
        # Add a label for each ingredient
        for i in dat:
            etiq=MyLabel(text=str(i),color= (0,0,0,1))
            scroll.add_widget(etiq)
            scroll.add_widget(MyCheckBox(size_hint_x=None, width=100))
        button_next = app.root.ids['ingredients'].ids['next']
        button_next.on_release = partial(self.cook, app=app, data=data['preparacion'])

    def icons(self, app):
        """Show all the icons on all toolbars of all screens
        Parameters
        ----------
        app: root app
        """
        icons_item = {
            "notebook-plus": "A\u00F1adir Receta",
            "notebook-edit": "Editar receta",
            "notebook-remove": "Eliminar receta",
        }
        list_recipes = app.root.ids['list_recipes'].ids['content_drawer'].ids['md_list']
        recipes = app.root.ids['recipes'].ids['content_drawer'].ids['md_list']
        ingredients = app.root.ids['ingredients'].ids['content_drawer'].ids['md_list']
        cooking = app.root.ids['cooking'].ids['content_drawer'].ids['md_list']
        category = app.root.ids['category'].ids['content_drawer'].ids['md_list']
        new_ingre = app.root.ids['new_ingre'].ids['content_drawer'].ids['md_list']
        submit = app.root.ids['submit'].ids['content_drawer'].ids['md_list']
        # Clear all widget of mdlist before to prevent duplicates
        list_recipes.clear_widgets(); recipes.clear_widgets();ingredients.clear_widgets();cooking.clear_widgets()
        category.clear_widgets();new_ingre.clear_widgets();submit.clear_widgets()
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
            category.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name], on_release=partial(self.icons_drawers_effects, option=icon_name,app=app))
            )
            new_ingre.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name], on_release=partial(self.icons_drawers_effects, option=icon_name,app=app))
            )
            submit.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name], on_release=partial(self.icons_drawers_effects, option=icon_name,app=app))
            )

    def icons_drawers_effects(self, caller, option, app):
        """Define the effects of the buttons in all toolbars. Show the categories to choose them
        Parameters
        ----------
        caller: require parameter of partial
        option: str
        app: root app
        """
        if option == 'notebook-edit':
            self.choose='edit'
            self.change_screen(app, 'category')
        elif option == 'notebook-remove':
            self.choose='delete'
            self.change_screen(app, 'category')
        else:
            self.choose='add'
            self.change_screen(app, 'category')

    def test(self, app, option):
        """Once the category is chosen, define the action to do on the next step
        Parameters
        ----------
        app: root app
        option: str
        """
        if self.choose == 'add':
            self.change_screen(app, 'new_ingre')
        elif self.choose == 'delete' :
            self.listado(app, option, 'delete')
        else:
            self.listado(app, option, 'edit')
        
    def delete(self, caller, category, title, app):
        """Delete a recipe of the database and restart the app (information)
        Parameters
        ----------
        caller: require parameter of partial
        category: str
        title: str
        app: root app
        """
        self.data_base.delete(category, title)
        app.on_start()

    def edit(self, caller, title, data, app):
        """Put all the data of one recipe on all the new recipe screens
        Parameters
        ----------
        caller: require parameter of partial
        title: str
        data: list of str
        app: root app
        """
        app.root.ids['new_ingre'].ids['titulo'].text=title
        scroll = app.root.ids['new_ingre'].ids['l_recipe']
        app.root.ids['submit'].ids['cooking_input'].text = data['preparacion']
        self.change_screen(app,'new_ingre')
        for ingre in data['ingredientes'].split(";"):
            text=MyTextInput(text=ingre)
            scroll.add_widget(text)

# Class for screens
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

class New_ingre(Screen):
    pass

class Submit(Screen):
    pass

class Category(Screen):
    pass

# All class for custom widgets
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

class ContentNavigationDrawer(BoxLayout):
    pass

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item.
        Set the color of the icon and text for the menu item.
        """
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color