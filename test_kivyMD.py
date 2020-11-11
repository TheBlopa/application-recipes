from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior, ThemeManager
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.label import MDLabel, MDIcon
from functools import partial
from kivy.uix.button import Button, ButtonBehavior
from kivy.core.window import Window
Window.size = (600, 800)

class ContentNavigationDrawer(BoxLayout):
    pass

class ImageButton(ButtonBehavior, Image):
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

# GUI = Builder.load_file("test_kivyMD.kv", encoding="utf-8")

class TestNavigationDrawer(MDApp):
    def build(self):
        return Builder.load_file("test_kivyMD.kv")

    def on_start(self):
        icons_item = {
            "notebook-edit": "Editar receta",
            "notebook-remove": "Eliminar receta",
            "notebook-plus": "A\u00F1adir Receta",
        }
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name], on_release=partial(self.receta, option=icon_name))
            )
    
    def receta(self, caller, option):
        if option == 'notebook-edit':
            print('editar')
        elif option == 'notebook-remove':
            print('eliminar')
        else:
            print('a\u00F1adir')


TestNavigationDrawer().run()