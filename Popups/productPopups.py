from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList, ThreeLineAvatarIconListItem, TwoLineIconListItem, TwoLineAvatarIconListItem
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
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton, MDRectangleFlatIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dropdownitem import MDDropDownItem
from functools import partial


class ProductPopup(Popup):
    def __init__(self, product, MDlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = f"{product.name}"
        self.MDlist = MDlist
        self.product = product
        self.size_hint = (0.7, 0.9)
    
        layout = BoxLayout()
        layout.orientation = "vertical"

        layout.add_widget(Label(text=f"Product: {product.name}", size_hint=(1,0.3)))
        layout.add_widget(Label(text=f"Cost: £{round(product.cost, 2)}", size_hint=(1,0.3)))

        scroll = ScrollView()
        self.Mlist = MDList()
        self.build_list()

        scroll.add_widget(self.Mlist)
        layout.add_widget(scroll)

        btn_layout = BoxLayout(size_hint=(1,0.3))
        btn_layout.add_widget(MDRectangleFlatButton(text="Return", on_release=self.dismiss))
        btn_layout.add_widget(MDRectangleFlatButton(text="Discard", on_release=self.discard_product))
        layout.add_widget(btn_layout)
        self.content = layout

    def discard_product(self, td):
        app = MDApp.get_running_app()
        app.customconfig.remove_product(self.product.name)
        self.MDlist()
        self.dismiss()

    def build_list(self):
        self.Mlist.clear_widgets()
        app = MDApp.get_running_app()
        for i in self.product.materials:
            item = MaterialListItem(i, self.build_list)
            item.text = f"{i.name}"
            item.secondary_text = f"Cost: £{round(i.unit_price, 2)}"
            icon = IconRightWidget(icon="layers-outline")
            icon.bind(on_release=item.show_popup)
            item.add_widget(icon)
            item.bind(on_release=item.show_popup)
            self.Mlist.add_widget(item)


class ProductActionPopup(Popup):
    def __init__(self, Mlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
        self.title = f"New Product"
        self.P_list = Mlist
        self.size_hint = (0.7, 0.9)
        self.materials_list = self.app.customconfig.load_materials()

        self.selected_materials_list = []
        app = MDApp.get_running_app()
        
        vlayout = BoxLayout()
        vlayout.orientation = "vertical"

        # name 
        namerow = BoxLayout(size_hint=(1, 0.25))
        namerow.orientation = "horizontal"
        namerow.add_widget(Label(text="Product name: "))
        self.name_widget = MDTextField()
        namerow.add_widget(self.name_widget)

        scroll = ScrollView()
        self.Mlist = MDList()
        self.build_list()

        scroll.add_widget(self.Mlist)

        material_chooser_layout = BoxLayout()
        material_chooser_layout.orientation = "horizontal"
        material_chooser_layout.size_hint = (1, 0.2)

        self.menu_items = self.build_material_chooser_list()

        self.add_material_btn = MDRectangleFlatIconButton()
        self.add_material_btn.text = "Material"
        self.add_material_btn.icon = "plus"
        self.add_material_menu = MDDropdownMenu(items=self.menu_items, width_mult=4, caller=self.add_material_btn, callback=self.add_material_callback)
        self.add_material_btn.on_release = self.add_material_menu.open

        self.remove_material_btn = MDRectangleFlatIconButton()
        self.remove_material_btn.text = "Material"
        self.remove_material_btn.icon = "minus"
        self.remove_material_menu = MDDropdownMenu(items=self.menu_items, width_mult=4, caller=self.remove_material_btn, callback=self.remove_material_callback)
        self.remove_material_btn.on_release = self.remove_material_menu.open

        material_chooser_layout.add_widget(self.add_material_btn)
        material_chooser_layout.add_widget(self.remove_material_btn)

        vlayout.add_widget(namerow)
        vlayout.add_widget(material_chooser_layout)
        vlayout.add_widget(scroll)

        buttonlayout = BoxLayout()
        buttonlayout.orientation = "horizontal"
        buttonlayout.size_hint = (1, 0.2)
        buttonlayout.add_widget(MDRectangleFlatButton(text="Discard", on_release=self.dismiss))
        buttonlayout.add_widget(MDRectangleFlatButton(text="Save", on_release=self.save))
        vlayout.add_widget(buttonlayout)
        self.content = vlayout

    def on_dismiss(self):
        self.Mlist.clear_widgets()
        self.selected_materials_list = []
        self.P_list()
        self.name_widget.text = ""

    def add_material_callback(self, item):
        for i in self.materials_list:
            if i.name == item.text:
                self.selected_materials_list.append(i)
        self.build_list()
        self.add_material_menu.dismiss()

    def remove_material_callback(self, item):
        try:
            for i in self.materials_list:
                if i.name == item.text:
                    self.selected_materials_list.remove(i)
        except ValueError:
            # Material not in product
            pass
        self.build_list()
        self.remove_material_menu.dismiss()
        
    def build_material_chooser_list(self):
        tmp = []
        for i in self.materials_list:
            tmp.append({
                "text": i.name
            })
        return tmp
            

    def build_list(self):
        self.Mlist.clear_widgets()
        app = MDApp.get_running_app()
        for i in self.selected_materials_list:
            item = MaterialListItem(i, self.build_list)
            item.text = f"{i.name}"
            item.secondary_text = f"Cost: £{round(i.unit_price, 2)}"
            icon = IconRightWidget(icon="layers-outline")
            icon.bind(on_release=item.show_popup)
            item.add_widget(icon)
            item.bind(on_release=item.show_popup)
            self.Mlist.add_widget(item)

    def save(self, td):
        app = MDApp.get_running_app()
        app.customconfig.new_product(self.name_widget.text, [i.name for i in self.selected_materials_list])
        self.P_list()
        self.dismiss()

class MaterialListItem(TwoLineAvatarIconListItem):
    def __init__(self, order, MDlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = order
        self.theme_text_color = "Custom"
        self.text_color = (1, 1, 1, 1)
        self.secondary_theme_text_color = "Custom"
        self.secondary_text_color = (1, 1, 1, 1)
        self.popup = MaterialPopup(order, MDlist)
    
    def show_popup(self, dt):
        self.popup.open()


class MaterialPopup(Popup):
    def __init__(self, material, MDlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = f"{material.name}"
        self.size_hint = (0.7, 0.9)
        self.material = material
        self.MDlist = MDlist

        layout = BoxLayout()
        layout.orientation = "vertical"

        layout.add_widget(Label(text=f"Quantity: {material.quantity}"))
        layout.add_widget(Label(text=f"Cost: £{str(round(material.unit_price, 2))}"))
        layout.add_widget(Label(text=f"Supplier: {material.supplier}"))
        btn_layout = BoxLayout()
        btn_layout.add_widget(MDRectangleFlatButton(text="Return", on_release=self.dismiss))

        layout.add_widget(btn_layout)
        self.content = layout