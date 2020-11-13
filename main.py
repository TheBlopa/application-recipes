from kivy.lang import Builder
from kivymd.app import MDApp
from manageDatabase import manageDatabase
from applicationMethods import ApplicationMethods


class MainApp(MDApp):
    """Main app to call all the functionality
    Parameters
    ----------
    MDApp: root app from kivyMD"""
    # def __init__(self, **kwargs):
    #     super(MainApp, self).__init__(**kwargs)
    #     Window.bind(on_keyboard=self.on_key)
        
    def build(self):
        """Define the database to use and the class with all the methods
        Returns
        -------
            Build the interfaces"""
        self.database = manageDatabase()
        self.application = ApplicationMethods(self.database)
        return Builder.load_file("kv/main.kv")

    def on_start(self):
        """Get all the information of the database, set the icons of all screens and change to the main screen"""
        self.data = self.database.get()
        self.application.icons(self)
        self.application.change_screen(self,"list_recipes")
    


    # def on_key(self, window, key, *args):
    #     """Function of back button on the device
    #     Parameters
    #     ----------
    #     window: object taht represent the keyboard of a device
    #     key: int"""
    #     if key == 27:  # the esc key
    #         self.change_screen('home_screen')


if __name__ == "__main__":
    """Run the App"""
    MainApp().run()