from datetime import datetime


class Material:
    def __init__(self, name, cost, quantity, supplier):
        self.name = name 
        self.quantity = quantity
        self.cost = cost
        self.unit_price = cost / quantity
        self.supplier = supplier

    @classmethod
    def from_db(cls, item):
        if item:
            return cls(item["name"], float(item["cost"]), int(item["quantity"]), item["supplier"])
        else:
            return None

    def __str__(self):
        return f"{self.name},{self.cost},{self.quantity},{self.supplier}"

