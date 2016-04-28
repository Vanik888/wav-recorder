# -*- coding: utf-8 -*-

class BaseOrderItem():
    def __init__(self, name, price, count, description, image_path):
        self.name = name
        self.price = price
        self.count = count
        self.description = description
        self.image_path = image_path

    def reset(self):
        self.count = 0

    def get_full_price(self):
        return self.price*self.count


