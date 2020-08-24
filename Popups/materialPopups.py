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



class MaterialPopup(Popup):
    def __init__(self, material, MDlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = f"{material.name}"
        self.size_hint = (0.6, 0.8)
        self.material = material
        self.MDlist = MDlist

        layout = BoxLayout()
        layout.orientation = "vertical"

        layout.add_widget(Label(text=f"Quantity: {material.quantity}"))
        layout.add_widget(Label(text=f"Cost: £{str(round(material.cost, 2))}"))
        layout.add_widget(Label(text=f"Supplier: {material.supplier}"))
        btn_layout = BoxLayout()
        btn_layout.add_widget(MDRectangleFlatButton(text="Return", on_release=self.dismiss))
        btn_layout.add_widget(MDRectangleFlatButton(text="Discard", on_release=self.discard_material))

        layout.add_widget(btn_layout)
        self.content = layout

    def discard_material(self, td):
        app = MDApp.get_running_app()
        app.customconfig.remove_material(self.material.name)
        self.MDlist()
        self.dismiss()



class MaterialActionPopup(Popup):
    def __init__(self, Mlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = f"New Material"
        self.Mlist = Mlist
        self.size_hint = (0.6, 0.7)
        app = MDApp.get_running_app()
        
        vlayout = BoxLayout()
        vlayout.orientation = "vertical"
        # name 
        namerow = BoxLayout(size_hint=(1, 0.25))
        namerow.orientation = "horizontal"
        namerow.add_widget(Label(text="Material name: "))
        self.name_widget = MDTextField()
        namerow.add_widget(self.name_widget)
        #cost
        costrow = BoxLayout(size_hint=(1, 0.25))
        costrow.orientation = "horizontal"
        costrow.add_widget(Label(text="Cost: "))
        self.cost_widget = MDTextField(color_mode='accent', line_color_normal=app.theme_cls.accent_color)
        costrow.add_widget(self.cost_widget)
        # quantity
        quantityrow = BoxLayout(size_hint=(1, 0.25))
        quantityrow.orientation = "horizontal"
        quantityrow.add_widget(Label(text="Quantity: "))
        self.quantity_widget = MDTextField(color_mode='accent', line_color_normal=app.theme_cls.accent_color)
        quantityrow.add_widget(self.quantity_widget)
        # supplier
        supplierrow = BoxLayout(size_hint=(1, 0.25))
        supplierrow.orientation = "horizontal"
        supplierrow.add_widget(Label(text="Supplier: "))
        self.supplier_widget = MDTextField(color_mode='accent', line_color_normal=app.theme_cls.accent_color)
        supplierrow.add_widget(self.supplier_widget)
        
        vlayout.add_widget(namerow)
        vlayout.add_widget(costrow)
        vlayout.add_widget(quantityrow)
        vlayout.add_widget(supplierrow)

        buttonlayout = BoxLayout()
        buttonlayout.orientation = "horizontal"
        buttonlayout.add_widget(MDRectangleFlatButton(text="Discard", on_release=self.dismiss))
        buttonlayout.add_widget(MDRectangleFlatButton(text="Save", on_release=self.save))
        vlayout.add_widget(buttonlayout)
        self.content = vlayout

    def save(self, td):
        app = MDApp.get_running_app()
        app.customconfig.new_material(self.name_widget.text, self.cost_widget.text, self.quantity_widget.text, self.supplier_widget.text)
        self.Mlist()
        self.name_widget.text = ""
        self.cost_widget.text = ""
        self.quantity_widget.text = ""
        self.supplier_widget.text = ""
        self.dismiss()