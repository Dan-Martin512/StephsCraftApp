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
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker
from kivy.clock import Clock


class OrderPopup(Popup):
    def __init__(self, order, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = f"Order {str(order.order_number)}"
        self.order = order
        app = MDApp.get_running_app()
        scroll = ScrollView()
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
        layout.add_widget(Label(text=f"Customer Cost: {order.customer_price}"))
        layout.add_widget(Label(text=f"Markup %: {order.markup}"))
        layout.add_widget(Label(text=f"Order Date: {order.order_date}"))
        layout.add_widget(Label(text=f"Quoted Lead Time: {str(order.leadtime)}"))
        layout.add_widget(Label(text=f"Origin: {order.origin}"))
        
        """ PAYMENT """
        payment_layout = BoxLayout()
        payment_layout.add_widget(Label(text=f"Payment: "))
        self.payment_btn = MDRectangleFlatButton(text=self.order.payment)
        self.payment_menu = MDDropdownMenu(items=self.build_paymentEntrys(app), width_mult=4, caller=self.payment_btn, callback=self.payment_callback)
        self.payment_btn.on_release = self.payment_menu.open
        payment_layout.add_widget(self.payment_btn)

        layout.add_widget(payment_layout)

        """ STATUS """
        status_layout = BoxLayout()
        status_layout.add_widget(Label(text=f"Status: "))
        self.status_btn = MDRectangleFlatButton(text=self.order.status)
        self.status_menu = MDDropdownMenu(items=self.build_statusEntrys(app), width_mult=4, caller=self.status_btn, callback=self.status_callback)
        self.status_btn.on_release = self.status_menu.open
        status_layout.add_widget(self.status_btn)

        layout.add_widget(status_layout)

        """ DELIVERY """
        delivery_layout = BoxLayout()
        delivery_layout.add_widget(Label(text="Delivery Method: "))
        self.delivery_btn = MDRectangleFlatButton(text=self.order.delivery)
        self.delivery_menu = MDDropdownMenu(items=self.build_deliveryEntrys(app), width_mult=4, caller=self.delivery_btn, callback=self.delivery_callback)
        self.delivery_btn.on_release = self.delivery_menu.open
        delivery_layout.add_widget(self.delivery_btn)

        layout.add_widget(delivery_layout)
        
        buttonlayout = BoxLayout()
        buttonlayout.orientation = "horizontal"
        buttonlayout.add_widget(MDRectangleFlatButton(text="Return", on_release=self.dismiss))
        buttonlayout.add_widget(MDRectangleFlatButton(text="Cancel Order", on_release=self.cancelOrder))
        layout.add_widget(buttonlayout)
        scroll.add_widget(layout)
        self.content = scroll

    def cancelOrder(self, td):
        print("Cancel Order")
        
    def validate_markup(self):
        self.order.markup = float(self.markup.text)/100
        self.customer_cost.text = str(self.order.customer_price)

    def validate_customer_cost(self):
        self.order.customer_price = float(self.customer_cost.text)
        self.markup.text = str(self.order.markup * 100)

    def build_paymentEntrys(self, app):
        origins = app.customconfig.get_setting("Payments")
        tmp = []
        for i in origins:
            tmp.append({"text": i})
        return tmp

    def payment_callback(self, btn):
        self.payment_btn.text = btn.text
        self.payment_menu.dismiss()

    def build_statusEntrys(self, app):
        origins = app.customconfig.get_setting("Status")
        tmp = []
        for i in origins:
            tmp.append({"text": i})
        return tmp

    def status_callback(self, btn):
        self.status_btn.text = btn.text
        self.status_menu.dismiss()

    def build_deliveryEntrys(self, app):
        origins = app.customconfig.get_setting("Delivery")
        tmp = []
        for i in origins:
            tmp.append({"text": i})
        return tmp

    def delivery_callback(self, btn):
        self.delivery_btn.text = btn.text
        self.delivery_menu.dismiss()


class OrderListItem(ThreeLineAvatarIconListItem):
    def __init__(self, order, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = order
        self.popup = OrderPopup(order)
    
    def show_popup(self, dt):
        self.popup.open()


class OrderActionPopup(Popup):
    def __init__(self, products, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = "New Order"
        app = MDApp.get_running_app()
        self.layout = BoxLayout(size_hint_y=2)
        self.scroll = ScrollView()
        #self.scroll.do_scroll_y = True

        self.layout.orientation = "vertical"

        self.available_products = products #app.customconfig.load_products()
        self.product_cost = 0
        self.products_selected = []
        self.markup = 0.2

        """ CUSTOMER NAME """
        customer_layout = BoxLayout()
        customer_layout.add_widget(Label(text=f"Customer:"))
        self.customer_input = MDTextField(color_mode='accent')
        customer_layout.add_widget(self.customer_input)
        self.layout.add_widget(customer_layout)

        """ CUSTOMER EMAIL """
        email_layout = BoxLayout()
        email_layout.add_widget(Label(text=f"Email:"))
        self.email_input = MDTextField(color_mode='accent')
        email_layout.add_widget(self.email_input)
        self.layout.add_widget(email_layout)

        """ PRODUCTS """
        product_title_layout = BoxLayout()
        product_title_layout.add_widget(Label(text=f"Products: "))

        self.add_prod_btn = MDRectangleFlatButton(text="Add Product")
        self.add_prod_menu = MDDropdownMenu(items=self.build_available_products(), width_mult=4, caller=self.add_prod_btn, callback=self.add_prod_callback)
        self.add_prod_btn.on_release = self.add_prod_menu.open
        
        product_title_layout.add_widget(self.add_prod_btn)
        self.product_list_layout = GridLayout()
        self.product_list_layout.cols = 3 
        
        self.layout.add_widget(product_title_layout)
        self.layout.add_widget(self.product_list_layout)

        
        """ MATERIAL COST """
        self.Material_cost = Label(text=f"Material Cost: £0")
        self.layout.add_widget(self.Material_cost)
        
        """ CUSTOMER COST """
        self.customer_cost = MDTextField(color_mode='accent')
        self.customer_cost.on_text_validate = self.validate_customer_cost
        cc_layout = BoxLayout()
        cc_layout.add_widget(Label(text="Customer Cost:"))
        cc_layout.add_widget(self.customer_cost)
        self.layout.add_widget(cc_layout)
        

        """ MARKUP """
        default_markup = app.customconfig.get_setting("Markup")
       
        self.markup = MDTextField(color_mode='accent', text=str(default_markup))
        self.markup.on_text_validate = self.validate_markup
        m_layout = BoxLayout()
        m_layout.add_widget(Label(text="Markup %"))
        m_layout.add_widget(self.markup)
        self.layout.add_widget(m_layout)  

        """ ORDER DATE """
        date_layout = BoxLayout()
        date_layout.add_widget(Label(text=f"Order Date: "))
        self.picker = MDDatePicker(callback=self.date_callback)
        self.picker_btn = MDRectangleFlatButton(text=str(self.picker.today) ,on_release=self.picker.open)
        date_layout.add_widget(self.picker_btn)
        self.layout.add_widget(date_layout)

        """ LEAD TIME """
        lead_layout = BoxLayout()
        lead_layout.add_widget(Label(text=f"Quoted Lead Time (Days): "))
        self.leadtime_btn = MDRectangleFlatButton(text="7")
        self.leadtime_menu = MDDropdownMenu(items=self.build_leadTimeEntrys(app), width_mult=4, caller=self.leadtime_btn, callback=self.leadtime_callback)
        self.leadtime_btn.on_release = self.leadtime_menu.open
        lead_layout.add_widget(self.leadtime_btn)

        self.layout.add_widget(lead_layout)

        """ ORIGIN """
        origin_layout = BoxLayout()
        origin_layout.add_widget(Label(text=f"Origin: "))
        self.origin_btn = MDRectangleFlatButton(text="Facebook")
        self.origin_menu = MDDropdownMenu(items=self.build_originEntrys(app), width_mult=4, caller=self.origin_btn, callback=self.origin_callback)
        self.origin_btn.on_release = self.origin_menu.open
        origin_layout.add_widget(self.origin_btn)

        self.layout.add_widget(origin_layout)

        """ PAYMENT """
        payment_layout = BoxLayout()
        payment_layout.add_widget(Label(text=f"Payment: "))
        self.payment_btn = MDRectangleFlatButton(text="Unpaid")
        self.payment_menu = MDDropdownMenu(items=self.build_paymentEntrys(app), width_mult=4, caller=self.payment_btn, callback=self.payment_callback)
        self.payment_btn.on_release = self.payment_menu.open
        payment_layout.add_widget(self.payment_btn)

        self.layout.add_widget(payment_layout)

        """ STATUS """
        status_layout = BoxLayout()
        status_layout.add_widget(Label(text=f"Status: "))
        self.status_btn = MDRectangleFlatButton(text="Order Placed")
        self.status_menu = MDDropdownMenu(items=self.build_statusEntrys(app), width_mult=4, caller=self.status_btn, callback=self.status_callback)
        self.status_btn.on_release = self.status_menu.open
        status_layout.add_widget(self.status_btn)

        self.layout.add_widget(status_layout)

        """ DELIVERY """
        delivery_layout = BoxLayout()
        delivery_layout.add_widget(Label(text="Delivery Method: "))
        self.delivery_btn = MDRectangleFlatButton(text="Collection")
        self.delivery_menu = MDDropdownMenu(items=self.build_deliveryEntrys(app), width_mult=4, caller=self.delivery_btn, callback=self.delivery_callback)
        self.delivery_btn.on_release = self.delivery_menu.open
        delivery_layout.add_widget(self.delivery_btn)

        self.layout.add_widget(delivery_layout)
        

        """ SAVE | DISCARD """
        buttonlayout = BoxLayout()
        buttonlayout.orientation = "horizontal"
        buttonlayout.add_widget(MDRectangleFlatButton(text="Discard", on_release=self.dismiss))
        buttonlayout.add_widget(MDRectangleFlatButton(text="Save Order", on_release=self.save))

        self.update_costing()
        self.layout.add_widget(buttonlayout)
        self.scroll.add_widget(self.layout)
        self.content = self.scroll

    def cancelOrder(self, td):
        print("Cancel Order")
        
    def validate_markup(self):
        try:
            if self.markup.text == "":
                self.markup.text = "0"
            self.update_costing()
        except ValueError:
            self.markup.text = "0"
            self.validate_markup()

    def validate_customer_cost(self):
        try:
            if self.customer_cost == "":
                self.customer_cost.text = "0"
            p_cost = self.Material_cost.text.replace("Material Cost: £", "")
            if float(p_cost) == 0:
                self.markup.text = "0"
                return
            self.markup.text = str(round(((float(self.customer_cost.text) - float(p_cost)) / float(p_cost))*100, 2))
        except ValueError:
            self.customer_cost.text = "0"
            self.validate_customer_cost()
        

    def save(self, td):
        print("Save New order")

    def build_available_products(self):
        tmp = []
        for i in self.available_products:
            tmp.append({
                "text": i.name
            })
        return tmp

    def add_prod_callback(self, prod):
        for i in self.available_products:
            if i.name == prod.text:
                self.products_selected.append(i)
        self.product_list_layout.clear_widgets()

        for i in self.products_selected:
            self.product_list_layout.add_widget(MDRoundFlatButton(text=i.name))

        self.update_costing()
        self.layout.do_layout()

        self.add_prod_menu.dismiss()


    def update_costing(self):
        cost = 0
        for i in self.products_selected:
            cost += i.cost
        cost = round(cost, 2)
        self.Material_cost.text = f"Material Cost: £{cost}"
        if cost == 0:
            self.customer_cost.text = "0"
            return
        self.customer_cost.text = str(round(cost + (cost * (float(self.markup.text)/100)), 2))


    def date_callback(self, date):
        self.picker_btn.text = str(date)

    def build_leadTimeEntrys(self, app):
        leadtime_range = app.customconfig.get_setting("Leadtime_max")
        tmp = []
        for i in range(int(leadtime_range)):
            tmp.append({
                "text": str(i)
            })
        return tmp

    def leadtime_callback(self, btn):
        self.leadtime_btn.text = btn.text
        self.leadtime_menu.dismiss()

    def build_originEntrys(self, app):
        origins = app.customconfig.get_setting("Origins")
        tmp = []
        for i in origins:
            tmp.append({"text": i})
        return tmp

    def origin_callback(self, btn):
        self.origin_btn.text = btn.text
        self.origin_menu.dismiss()

    def build_paymentEntrys(self, app):
        origins = app.customconfig.get_setting("Payments")
        tmp = []
        for i in origins:
            tmp.append({"text": i})
        return tmp

    def payment_callback(self, btn):
        self.payment_btn.text = btn.text
        self.payment_menu.dismiss()

    def build_statusEntrys(self, app):
        origins = app.customconfig.get_setting("Status")
        tmp = []
        for i in origins:
            tmp.append({"text": i})
        return tmp

    def status_callback(self, btn):
        self.status_btn.text = btn.text
        self.status_menu.dismiss()

    def build_deliveryEntrys(self, app):
        origins = app.customconfig.get_setting("Delivery")
        tmp = []
        for i in origins:
            tmp.append({"text": i})
        return tmp

    def delivery_callback(self, btn):
        self.delivery_btn.text = btn.text
        self.delivery_menu.dismiss()