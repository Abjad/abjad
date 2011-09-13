from abjad import *
from abjad.tools.marktools import LilyPondCommandMark


def test_LilyPondCommandMark___repr___01():
    '''Repr of unattached LilyPond command mark is evaluable.
    '''

    lily_pond_command_mark_1 = marktools.LilyPondCommandMark('break')
    lily_pond_command_mark_2 = eval(repr(lily_pond_command_mark_1))

    assert isinstance(lily_pond_command_mark_1, marktools.LilyPondCommandMark)
    assert isinstance(lily_pond_command_mark_2, marktools.LilyPondCommandMark)
    assert lily_pond_command_mark_1 == lily_pond_command_mark_2
