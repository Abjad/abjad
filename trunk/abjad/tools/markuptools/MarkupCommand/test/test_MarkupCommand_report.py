from abjad import *


def test_MarkupCommand_report_01():

    a = markuptools.MarkupCommand('draw-circle', ['#1', '#0.1', '##f'], None)
    b = markuptools.MarkupCommand('line', None, ['one', 'two', 'three'])
    c = markuptools.MarkupCommand('rounded-box', None, [b])
    d = markuptools.MarkupCommand('combine', None, [a, c], is_braced = False)
    e = markuptools.MarkupCommand('rotate', ['45'], [d])
    f = markuptools.MarkupCommand('triangle', [schemetools.SchemeBoolean(False)], None)
    g = markuptools.MarkupCommand('concat', None, [e, f])

    assert g.report(output = False) == '\\concat {\n\t\\rotate 45\n\t\t\\combine\n\t\t\t\\draw-circle #1 #0.1 ##f\n\t\t\t\\rounded-box\n\t\t\t\t\\line {\n\t\t\t\t\tone\n\t\t\t\t\ttwo\n\t\t\t\t\tthree\n\t\t\t\t}\n\t\\triangle ##f\n}'
