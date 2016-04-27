# -*- coding: utf-8 -*-

from menu.dishes.base_dish import BaseDish

class TuttyFrutty(BaseDish):
    def __init__(self):
        self.price = 420
        self.count = 0
        self.name = 'Тутти Фрутти'
        self.description = 'с молочным шоколадом, ягодами и мороженым'
        self.image_path = './stat/inteface_images/tutty_frutty_400_300.png'


