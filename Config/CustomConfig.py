import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
from OrderComponents.Order import Order
from OrderComponents.Product import Product
from OrderComponents.Material import Material



class DBconfig():
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('Order_db')

    def load_settings(self):
        return [i for i in self.table.query(KeyConditionExpression=Key('type').eq("Setting"))["Items"]]

    def get_setting(self, name):
        try:
            return self.table.get_item(Key={"name": name, "type": "Setting"})["Item"]["value"]
        except KeyError:
            return None

    def load_orders(self):
        return [Order.from_db(i, self) for i in self.table.query(KeyConditionExpression=Key('type').eq("Order"))["Items"]]

    def get_order(self, name):
        try:
            return Order.from_db(self.table.get_item(Key={"name": name, "type": "Order"})["Item"], self)
        except KeyError:
            return None  

    def load_products(self):
        return [Product.from_db(i, self) for i in self.table.query(KeyConditionExpression=Key('type').eq("Product"))["Items"]]

    def get_product(self, name):
        try:
            return Product.from_db(self.table.get_item(Key={"name": name, "type": "Product"})["Item"], self)
        except KeyError:
            return None        

    def load_materials(self):
        return [Material.from_db(i) for i in self.table.query(KeyConditionExpression=Key('type').eq("Material"))["Items"]]

    def get_material(self, name):
        try:
            return Material.from_db(self.table.get_item(Key={"name": name, "type": "Material"})["Item"])
        except KeyError:
            return None

    def remove_material(self, name):
        self.table.delete_item(
            Key={
                'name': name,
                'type': 'Material'
                }
            )

    def remove_product(self, name):
        self.table.delete_item(
            Key={
                'name': name,
                'type': 'Product'
                }
            )

    def remove_order(self, name):
        self.table.delete_item(
            Key={
                'name': name,
                'type': 'Order'
                }
            )

    def new_material(self, name, cost, quantity, supplier):
        self.table.put_item(
            Item={
                'type': "Material",
                'name': name,
                'cost': cost,
                'quantity': quantity,
                'supplier': supplier
                }
            )
    
    def new_product(self, name, materials):
        self.table.put_item(
            Item={
                'type': "Product",
                'name': name,
                'materials': materials
                }
            )

    def new_order(self, customer, product, leadtime, order_date, status, comments, origin, payment, email, markup):
        self.table.put_item(
            Item={
                'type': "Order",
                'customer': customer,
                'product': product,
                'leadtime': leadtime,
                'orderDate': order_date,
                "status": status,
                "markup": str(markup),
                "name": f"#{int(datetime.now().timestamp())}",
                "comments": comments,
                "origin": origin,
                "payment": payment,
                "email": email
                }
            )
    
    