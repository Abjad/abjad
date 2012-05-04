from abjad import *
from abjad.tools.markuptools.MarkupCommand import MarkupCommand


def test_MarkupCommand___repr___01():
    '''Repr is evaluable.
    '''

    markup_command_1 = markuptools.MarkupCommand('hspace', 0)
    markup_command_2 = eval(repr(markup_command_1))

    assert markup_command_1 is not markup_command_2
    assert markup_command_1 == markup_command_2

