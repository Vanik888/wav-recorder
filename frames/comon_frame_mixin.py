# -*- coding: utf-8 -*-

import textwrap


class CommonFrameMixin():
    def add_spaces_to_str(self, length, txt):
        while len(txt) != length:
            txt += ' '
        return txt

    def get_name_formated_by_lines(self, lenght, txt):
        return textwrap.fill(txt, lenght)
        #
        # formated = ''
        # for i,c in enumerate(txt):
        #     formated += c
        #     if i % lenght == 0 and i != 0:
        #         formated+='\n'
        # return formated


