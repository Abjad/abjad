from abjad import *


def test_MarkupCommand__get_format_pieces_01():

    circle = markuptools.MarkupCommand('draw-circle', 2.5, 0.1, False)
    square = markuptools.MarkupCommand('rounded-box', 'hello?')
    line = markuptools.MarkupCommand('line', [square, 'wow!'])
    rotate = markuptools.MarkupCommand('rotate', 60, line)
    combine = markuptools.MarkupCommand('combine', rotate, circle)

    assert combine._get_format_pieces(is_indented=True) == [
        '\\combine',
        '\t\\rotate',
        '\t\t#60',
        '\t\t\\line',
        '\t\t\t{',
        '\t\t\t\t\\rounded-box',
        '\t\t\t\t\thello?',
        '\t\t\t\twow!',
        '\t\t\t}',
        '\t\\draw-circle',
        '\t\t#2.5',
        '\t\t#0.1',
        '\t\t##f'
    ]
