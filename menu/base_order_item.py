# -*- coding: utf-8 -*-

class BaseOrderItem():
    def __init__(self, name, price, count, description, image_path):
        self.name = name
        self.price = price
        self.count = count
        self.description = description
        self.image_path = image_path
        self.count_limit = 20

    def add_item(self):
        if not (self.name == 'Официант' and self.count > 0):
            if self.count < self.count_limit:
                self.count += 1

    def remove_item(self):
        if self.count > 0:
            self.count -= 1

    def reset(self):
        self.count = 0

    def get_full_price(self):
        return self.price*self.count


