from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList, ThreeLineAvatarIconListItem
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFloatingActionButton
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import IconRightWidget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock


class SettingsScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

        app = MDApp.get_running_app()
        scroll = ScrollView()
        Mlist = MDList()
        
        layout = BoxLayout()
        layout.orientation = "vertical"
        toolbar = MDToolbar(title="Settings")
        toolbar.left_action_items = [
            ["menu", lambda x: self.openNav()]]
        layout.add_widget(toolbar)
        scroll.add_widget(Mlist)
        layout.add_widget(scroll)        
        self.add_widget(layout)

        
    def openNav(self):
        app = MDApp.get_running_app()
        app.root.ids.nav_drawer.toggle_nav_drawer()



class ProductListItem(ThreeLineAvatarIconListItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass