from datetime import datetime, timedelta
from OrderComponents.Product import Product



class Order:
    def __init__(self, order_num, customer, products, cost, leadtime, order_date, status, comments, origin, email, payment, delivery, markup=0.1):
        self.order_number = order_num
        self.order_date = order_date
        self.customer = customer
        self.product = products
        self._markup = markup
        self.status = status
        self.products_cost = cost
        self._customer_price =  float(cost) + (float(markup)*float(cost))
        self.leadtime = leadtime
        self.comments = comments
        self.delivery = delivery
        self.origin = origin 
        self.payment = payment 
        self.email = email

    @property
    def customer_price(self):
        return self._customer_price

    @customer_price.getter
    def customer_price(self):
        return float(self.products_cost) + (float(self.markup) * float(self.products_cost))

    @customer_price.setter
    def customer_price(self, val):
        self._customer_price = val
        self.markup = (float(val) - float(self.products_cost)) / float(self.products_cost)

    @property
    def markup(self):
        return self._markup

    @markup.getter
    def markup(self):
        return self._markup

    @markup.setter
    def markup(self, val):
        self._markup = val
        self._customer_price = float(self.products_cost) + (float(self.markup) * float(self.products_cost))

    @classmethod
    def from_db(cls, item, db):
        return cls(item["name"], item["customer"], item["products"], item["cost"], int(item["leadtime"]), item["orderDate"], item["status"], item["comments"], item["origin"], item["email"], item["payment"], item["delivery"], float(item["markup"]))

    def __str__(self):
        return f"{self.order_number},{self.customer},{self.products},{self.leadtime},{self.comments},{self.markup},{self.order_date}"
