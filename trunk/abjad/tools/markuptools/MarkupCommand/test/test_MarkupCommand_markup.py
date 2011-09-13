from abjad import *


def test_MarkupCommand_markup_01():
    mc = markuptools.MarkupCommand('rounded-box', None, ['one', 'two', 'three'])
    assert mc.markup == ('one', 'two', 'three')
