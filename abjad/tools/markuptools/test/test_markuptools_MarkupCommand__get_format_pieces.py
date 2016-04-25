# -*- coding: utf-8 -*-
from abjad import *


def test_markuptools_MarkupCommand__get_format_pieces_01():

    circle = markuptools.MarkupCommand('draw-circle', 2.5, 0.1, False)
    square = markuptools.MarkupCommand('rounded-box', 'hello?')
    line = markuptools.MarkupCommand('line', [square, 'wow!'])
    rotate = markuptools.MarkupCommand('rotate', 60, line)
    combine = markuptools.MarkupCommand('combine', rotate, circle)

    assert combine._get_format_pieces() == [
        '\\combine',
        '    \\rotate',
        '        #60',
        '        \\line',
        '            {',
        '                \\rounded-box',
        '                    hello?',
        '                wow!',
        '            }',
        '    \\draw-circle',
        '        #2.5',
        '        #0.1',
        '        ##f'
    ]
