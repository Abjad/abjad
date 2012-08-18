from abjad import *


def test_Markup__get_format_pieces_01():

    circle = markuptools.MarkupCommand('draw-circle', 2.5, 0.1, False)
    square = markuptools.MarkupCommand('rounded-box', 'hello?')
    line = markuptools.MarkupCommand('line', [square, 'wow!'])
    markup = markuptools.Markup(('X', circle, 'Y', line, 'Z'), direction=Up)

    assert markup._get_format_pieces(is_indented=True) == [
        '^ \\markup {',
        '\tX',
        '\t\\draw-circle',
        '\t\t#2.5',
        '\t\t#0.1',
        '\t\t##f',
        '\tY',
        '\t\\line',
        '\t\t{',
        '\t\t\t\\rounded-box',
        '\t\t\t\thello?',
        '\t\t\twow!',
        '\t\t}',
        '\tZ',
        '\t}'
    ]
