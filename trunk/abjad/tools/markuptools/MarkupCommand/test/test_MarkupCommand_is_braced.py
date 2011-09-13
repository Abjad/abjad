from abjad import *


def test_MarkupCommand_is_braced_01():
    mc = markuptools.MarkupCommand('rounded-box', None, ['one', 'two', 'three'])
    assert mc.is_braced == True


def test_MarkupCommand_is_braced_02():
    mc = markuptools.MarkupCommand('combine', None, ['one', 'two', 'three'], is_braced = False)
    assert mc.is_braced == False


def test_MarkupCommand_is_braced_03():
    mc = markuptools.MarkupCommand('concat', None, ['one', 'two', 'three'], is_braced = True)
    assert mc.is_braced == True
