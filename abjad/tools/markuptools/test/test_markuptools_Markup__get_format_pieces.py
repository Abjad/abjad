# -*- coding: utf-8 -*-
from abjad import *


def test_markuptools_Markup__get_format_pieces_01():

    circle = markuptools.MarkupCommand('draw-circle', 2.5, 0.1, False)
    square = markuptools.MarkupCommand('rounded-box', 'hello?')
    line = markuptools.MarkupCommand('line', [square, 'wow!'])
    markup = markuptools.Markup(('X', circle, 'Y', line, 'Z'), direction=Up)

    assert markup._get_format_pieces() == [
        '^ \\markup {',
        '    X',
        '    \\draw-circle',
        '        #2.5',
        '        #0.1',
        '        ##f',
        '    Y',
        '    \\line',
        '        {',
        '            \\rounded-box',
        '                hello?',
        '            wow!',
        '        }',
        '    Z',
        '    }'
    ]
