import kivy
kivy.require('1.0.7')
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.icon_definitions import md_icons
from kivy.clock import Clock
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList, OneLineIconListItem
from kivy.properties import StringProperty

import time
import sys
from os import path, mkdir
import psutil
import pathlib 

from CustomScreens import OrderScreen, ProductsScreen, MaterialScreen, SettingsScreen
from Config import DBconfig


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")
    return path.join(base_path, relative_path)


class ScreenManagment(ScreenManager):
    pass

class ContentNavigationDrawer(BoxLayout):
    def on_kv_post(self, td):
        self.ids.md_list.add_widget(ItemDrawer(icon="alpha-o-circle-outline", text="Orders", screen= "Order_Screen"))
        self.ids.md_list.add_widget(ItemDrawer(icon="alpha-p-circle-outline", text="Products", screen= "Product_Screen"))
        self.ids.md_list.add_widget(ItemDrawer(icon="alpha-m-circle-outline", text="Materials", screen= "Material_Screen"))
        self.ids.md_list.add_widget(ItemDrawer(icon="settings", text="Settings", screen= "Settings_Screen"))

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    screen = StringProperty()

    def on_release(self):
        app = MDApp.get_running_app()
        app.root.ids.nav_drawer.set_state("close")
        app.root.ids.sm.current = self.screen

kv_string = """
<ItemDrawer>:
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)
    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color

<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"
    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height
        Image:
            id: avatar
            size_hint: None, None
            size: "200dp", "200dp"
            source: "Images\Logo.jpg"
    MDLabel:
        text: "Handmade Gifts By Steph"
        font_style: "Button"
        size_hint_y: None
        height: self.texture_size[1]
    MDLabel:
        text: "stephanieelouise@live.co.uk"
        font_style: "Caption"
        size_hint_y: None
        height: self.texture_size[1]
    ScrollView:
        DrawerList:
            id: md_list
            
Screen:
    NavigationLayout:
        ScreenManager:
            id: sm
            OrderScreen:
                name: "Order_Screen"
            ProductsScreen:
                name: "Product_Screen"
            MaterialScreen:
                name: "Material_Screen"
            SettingsScreen:
                name: "Settings_Screen"

        MDNavigationDrawer:
            id: nav_drawer
            ContentNavigationDrawer:

"""

class MainApp(MDApp):
    def __init__(self):
        super().__init__() 
        self.title = "Handmade Gifts By Steph"
        self.customconfig = DBconfig()

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(kv_string)

if __name__ == '__main__':

    MainApp().run()

    


