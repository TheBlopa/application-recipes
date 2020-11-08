from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivy.uix.button import ButtonBehavior

from kivy.uix.image import Image

class ContentNavigationDrawer(BoxLayout):
    pass

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))

class DrawerList(ThemableBehavior, MDList):
    pass
    # def set_color_item(self, instance_item):
    #     """Called when tap on a menu item."""

    #     # Set the color of the icon and text for the menu item.
    #     for item in self.children:
    #         if item.text_color == self.theme_cls.primary_color:
    #             item.text_color = self.theme_cls.text_color
    #             break
    #     instance_item.text_color = self.theme_cls.primary_color

class DemoApp(MDApp):

    def build(self):
        screen =Builder.load_file("test_kivyMD.kv", encoding="utf-8")
        return screen
    
    # def on_start(self):
    #     icons_item = {
    #         "folder": "My files",
    #         "account-multiple": "Shared with me",
    #         "star": "Starred",
    #         "history": "Recent",
    #         "checkbox-marked": "Shared with me",
    #         "upload": "Upload",
    #     }
    #     for icon_name in icons_item.keys():
    #         self.root.ids.content_drawer.ids.md_list.add_widget(
    #             Image(source='icons/add.png')
    #         )


DemoApp().run()