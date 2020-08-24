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



class OrderScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

        app = MDApp.get_running_app()
        scroll = ScrollView()
        Mlist = MDList()

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
        OrderActionPopup().open()
        
    def openNav(self):
        app = MDApp.get_running_app()
        app.root.ids.nav_drawer.toggle_nav_drawer()



class OrderPopup(Popup):
    def __init__(self, order, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = f"Order {str(order.order_number)}"
        self.order = order
        app = MDApp.get_running_app()
        layout = BoxLayout()
        layout.orientation = "vertical"
        b_layout = GridLayout()
        b_layout.cols = 3
        b_layout.padding = 10

        layout.add_widget(Label(text=f"Customer: {order.customer}"))
        layout.add_widget(Label(text=f"Email: {order.email}"))
        layout.add_widget(Label(text=f"Products: "))
        for i in order.product:
            label = MDRoundFlatButton(text=i)
            label.pos_hint={"center_x": .5, "center_y": .5}
            label.text_color = app.theme_cls.accent_color
            b_layout.add_widget(label)
        layout.add_widget(b_layout)
        
        layout.add_widget(Label(text=f"Material Cost: £{round(order.products_cost, 2)}"))

        self.customer_cost = MDTextField(color_mode='accent', text=str(order.customer_price))
        self.markup = MDTextField(color_mode='accent', text=str(order.markup*100))
        self.markup.on_text_validate = self.validate_markup
        self.customer_cost.on_text_validate = self.validate_customer_cost
        
        cc_layout = BoxLayout()
        m_layout = BoxLayout()

        cc_layout.add_widget(Label(text="Customer Cost:"))
        cc_layout.add_widget(self.customer_cost)
        m_layout.add_widget(Label(text="Markup %"))
        m_layout.add_widget(self.markup)

        layout.add_widget(cc_layout)
        layout.add_widget(m_layout)
        #layout.add_widget(Label(text=f"Markup: {round(order.markup, 4)}"))

        
        layout.add_widget(Label(text=f"Order Date: {order.order_date}"))
        layout.add_widget(Label(text=f"Quoted Lead Time: {str(order.leadtime)}"))
        layout.add_widget(Label(text=f"Origin: {order.origin}"))
        layout.add_widget(Label(text=f"Payment: {order.payment}"))
        layout.add_widget(Label(text=f"Status: {order.status}"))
        
        buttonlayout = BoxLayout()
        buttonlayout.orientation = "horizontal"
        buttonlayout.add_widget(MDRectangleFlatButton(text="Return", on_release=self.dismiss))
        buttonlayout.add_widget(MDRectangleFlatButton(text="Cancel Order", on_release=self.cancelOrder))
        layout.add_widget(buttonlayout)
        self.content = layout

    def cancelOrder(self, td):
        print("Cancel Order")
        
    def validate_markup(self):
        self.order.markup = float(self.markup.text)/100
        self.customer_cost.text = str(self.order.customer_price)

    def validate_customer_cost(self):
        self.order.customer_price = float(self.customer_cost.text)
        self.markup.text = str(self.order.markup * 100)

class OrderListItem(ThreeLineAvatarIconListItem):
    def __init__(self, order, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = order
        self.popup = OrderPopup(order)
    
    def show_popup(self, dt):
        self.popup.open()


class OrderActionPopup(Popup):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = "New Order"
        app = MDApp.get_running_app()
        layout = BoxLayout()
        layout.orientation = "vertical"

        self.available_products = app.customconfig.load_products()

        self.product_cost = 0
        self.products_selected = []
        self.markup = 0.2

        """ CUSTOMER NAME """
        customer_layout = BoxLayout()
        customer_layout.add_widget(Label(text=f"Customer:"))
        self.customer_input = MDTextField(color_mode='accent')
        customer_layout.add_widget(self.customer_input)
        layout.add_widget(customer_layout)

        """ CUSTOMER EMAIL """
        email_layout = BoxLayout()
        email_layout.add_widget(Label(text=f"Email:"))
        self.email_input = MDTextField(color_mode='accent')
        email_layout.add_widget(self.email_input)
        layout.add_widget(email_layout)

        """ PRODUCTS """
        product_title_layout = BoxLayout()
        product_title_layout.add_widget(Label(text=f"Products: "))
        product_title_layout.add_widget(MDIconButton(icon="plus"))

        self.product_list_layout = BoxLayout()
        #add selected 
        
        layout.add_widget(product_title_layout)

        
        """ MATERIAL COST """
        self.Material_cost = Label(text=f"Material Cost: £")
        layout.add_widget(self.Material_cost)
        
        """ CUSTOMER COST """
        self.customer_cost = MDTextField(color_mode='accent')
        self.customer_cost.on_text_validate = self.validate_customer_cost
        cc_layout = BoxLayout()
        cc_layout.add_widget(Label(text="Customer Cost:"))
        cc_layout.add_widget(self.customer_cost)
        layout.add_widget(cc_layout)

        """ MARKUP """
        self.markup = MDTextField(color_mode='accent')
        self.markup.on_text_validate = self.validate_markup
        m_layout = BoxLayout()
        m_layout.add_widget(Label(text="Markup %"))
        m_layout.add_widget(self.markup)
        layout.add_widget(m_layout)  

        """ ORDER DATE """
        layout.add_widget(Label(text=f"Order Date: "))

        """ LEAD TIME """
        layout.add_widget(Label(text=f"Quoted Lead Time: "))

        """ ORIGIN """
        layout.add_widget(Label(text=f"Origin: "))

        """ PAYMENT """
        layout.add_widget(Label(text=f"Payment: "))

        """ STATUS """
        layout.add_widget(Label(text=f"Status: "))
        

        """ SAVE | DISCARD """
        buttonlayout = BoxLayout()
        buttonlayout.orientation = "horizontal"
        buttonlayout.add_widget(MDRectangleFlatButton(text="Discard", on_release=self.dismiss))
        buttonlayout.add_widget(MDRectangleFlatButton(text="Save Order", on_release=self.save))
        layout.add_widget(buttonlayout)
        self.content = layout

    def cancelOrder(self, td):
        print("Cancel Order")
        
    def validate_markup(self):
        #self.order.markup = float(self.markup.text)/100
        #self.customer_cost.text = str(self.order.customer_price)
        pass

    def validate_customer_cost(self):
        #self.order.customer_price = float(self.customer_cost.text)
        #self.markup.text = str(self.order.markup * 100)
        pass

    def save(self, td):
        print("Save New order")

    def build_available_products(self):
        pass
