# -*- coding: utf-8 -*-

import textwrap


class CommonFrameMixin():
    def get_bnt_font(self):
        return ('Helvetica', 16, 'bold')

    def add_spaces_to_str(self, length, txt):
        while len(txt) != length:
            txt += ' '
        return txt

    def get_name_formated_by_lines(self, lenght, txt):
        return textwrap.fill(txt, lenght)
