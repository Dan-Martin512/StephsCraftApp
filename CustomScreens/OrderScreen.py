from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList, ThreeLineAvatarIconListItem
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFloatingActionButton, MDRoundFlatButton, MDIconButton
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import IconRightWidget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.uix.textfield import MDTextField
from kivymd.uix.picker import MDDatePicker
from kivy.clock import Clock

from Popups import OrderPopup, OrderActionPopup, OrderListItem



class OrderScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

        app = MDApp.get_running_app()
        scroll = ScrollView()
        Mlist = MDList()
        self.products = app.customconfig.load_products()

        for i in app.customconfig.load_orders():
            item = OrderListItem(i)
            item.text = f"Order: {i.order_number}"
            item.secondary_text = f"Customer: {i.customer}"
            item.tertiary_text = f"Status: {i.status}"
            icon = IconRightWidget(icon="account-details")
            icon.bind(on_release=item.show_popup)
            item.add_widget(icon)
            item.bind(on_release=item.show_popup)
            Mlist.add_widget(item)
        
        layout = BoxLayout()
        layout.orientation = "vertical"
        toolbar = MDToolbar(title="Orders")
        toolbar.left_action_items = [
            ["menu", lambda x: self.openNav()]]
        layout.add_widget(toolbar)
        scroll.add_widget(Mlist)
        layout.add_widget(scroll)
        self.action = MDFloatingActionButton(icon="plus", pos_hint={"center_x":0.5}, on_release=self.openAction)
        layout.add_widget(self.action)
        
        self.add_widget(layout)

    def openAction(self, td):
        OrderActionPopup(self.products).open()
        
    def openNav(self):
        app = MDApp.get_running_app()
        app.root.ids.nav_drawer.toggle_nav_drawer()

