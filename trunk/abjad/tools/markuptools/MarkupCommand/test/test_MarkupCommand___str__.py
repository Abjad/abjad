from abjad import *


def test_MarkupCommand___str___01():

    a = markuptools.MarkupCommand('draw-circle', 1, 0.1, False)
    b = markuptools.MarkupCommand('line', ['one', 'two', 'three'])
    c = markuptools.MarkupCommand('rounded-box', b)
    d = markuptools.MarkupCommand('combine', a, c)
    e = markuptools.MarkupCommand('rotate', 45, d)
    f = markuptools.MarkupCommand('triangle', False)
    g = markuptools.MarkupCommand('concat', [e, f])

    assert str(g) == '\\concat { \\rotate #45 \\combine \\draw-circle #1 #0.1 ##f \\rounded-box \\line { one two three } \\triangle ##f }'
