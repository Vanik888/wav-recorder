# -*- coding: utf-8 -*-

from frames.comon_frame_mixin import CommonFrameMixin
from frames.base_order_page import BaseOrderPage


class DrinksPage(BaseOrderPage, CommonFrameMixin):
    def __init__(self, *args, **kwargs):
        BaseOrderPage.__init__(self,
                               root=kwargs['root'],
                               controller=kwargs['controller'],
                               frame_size=kwargs['frame_size'],
                               header_txt='Выбор напитков',
                               order_type='drinks')


