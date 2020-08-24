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
from kivymd.uix.textfield import MDTextField

from Popups import MaterialActionPopup, MaterialPopup


class MaterialScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

        app = MDApp.get_running_app()
        scroll = ScrollView()
        self.Mlist = MDList()
        self.build_list()

        layout = BoxLayout()
        layout.orientation = "vertical"
        toolbar = MDToolbar(title="Materials")
        toolbar.left_action_items = [
            ["menu", lambda x: self.openNav()]]
        layout.add_widget(toolbar)
        scroll.add_widget(self.Mlist)
        layout.add_widget(scroll)
        self.action_popup = MaterialActionPopup(self.build_list)
        self.action = MDFloatingActionButton(icon="plus", pos_hint={"center_x":0.5}, on_release=self.action_popup.open)
        layout.add_widget(self.action)
        self.add_widget(layout)

    def build_list(self):
        self.Mlist.clear_widgets()
        app = MDApp.get_running_app()
        for i in app.customconfig.load_materials():
            item = MaterialListItem(i, self.build_list)
            item.text = f"{i.name}"
            item.secondary_text = f"Cost: £{i.cost} Quantity: {i.quantity}"
            icon = IconRightWidget(icon="layers-outline")
            icon.bind(on_release=item.show_popup)
            item.add_widget(icon)
            item.bind(on_release=item.show_popup)
            self.Mlist.add_widget(item)
        
    def openNav(self):
        app = MDApp.get_running_app()
        app.root.ids.nav_drawer.toggle_nav_drawer()


class MaterialListItem(ThreeLineAvatarIconListItem):
    def __init__(self, order, MDlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = order
        self.popup = MaterialPopup(order, MDlist)
    
    def show_popup(self, dt):
        self.popup.open()
