# -*- coding: utf-8 -*-

class BaseDish():
    def __init__(self, price, count, name):
        self.price = price
        self.count = count
        self.name = name

    def reset(self):
        self.count = 0

    def get_full_price(self):
        return self.price*self.count
