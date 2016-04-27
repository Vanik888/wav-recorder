# -*- coding: utf-8 -*-

from menu.dishes.base_dish import BaseDish

class StrabberyNutsKrep(BaseDish):
    def __init__(self):
        self.price = 350
        self.count = 0
        self.name = 'Клубнично-ореховый креп'
        self.description = 'c шоколадом и мороженым'
        self.image_path = './stat/inteface_images/krep_klubnichno_orekhoviy.png'


