# -*- coding: utf-8 -*-

from menu.dishes.base_dish import BaseDish

class StrabberyNutsKrep(BaseDish):
    def __init__(self):
        BaseDish.__init__(self, price=420, count=0, name='Тутти Фрутти')
        self.image_path = './stat/inteface_images/krep_klubnichno_orekhoviy.png'


