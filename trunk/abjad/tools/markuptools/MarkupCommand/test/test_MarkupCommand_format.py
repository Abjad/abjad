from abjad import *


def test_MarkupCommand_format_01():

    a = markuptools.MarkupCommand('draw-circle', ['#1', '#0.1', '##f'], None)
    b = markuptools.MarkupCommand('line', None, ['one', 'two', 'three'])
    c = markuptools.MarkupCommand('rounded-box', None, [b])
    d = markuptools.MarkupCommand('combine', None, [a, c], is_braced = False)
    e = markuptools.MarkupCommand('rotate', ['45'], [d])
    f = markuptools.MarkupCommand('triangle', [schemetools.SchemeBoolean(False)], None)
    g = markuptools.MarkupCommand('concat', None, [e, f])

    assert g.format == '\\concat { \\rotate 45 \\combine \\draw-circle #1 #0.1 ##f \\rounded-box \\line { one two three } \\triangle ##f }'
