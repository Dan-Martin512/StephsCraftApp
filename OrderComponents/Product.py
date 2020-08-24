from datetime import datetime


class Product:
    def __init__(self, name, materials):
        self.materials = materials
        self.name = name
        self.cost = self.__cost_calc()
        
    def __cost_calc(self):
        cost = 0
        for i in self.materials:
            cost += i.unit_price
        return cost


    @classmethod
    def from_db(cls, item, db):
        materials = [db.get_material(i) for i in item["materials"]]
        return cls(item["name"], materials)
    
    def __str__(self):
        return f"{self.name},{[i.name for i in self.materials]}"

