# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.marktools import LilyPondCommand


def test_marktools_LilyPondCommand___repr___01():
    r'''Repr of unattached LilyPond command mark is evaluable.
    '''

    lily_pond_command_mark_1 = marktools.LilyPondCommand('break')
    lily_pond_command_mark_2 = eval(repr(lily_pond_command_mark_1))

    assert isinstance(lily_pond_command_mark_1, marktools.LilyPondCommand)
    assert isinstance(lily_pond_command_mark_2, marktools.LilyPondCommand)
    assert lily_pond_command_mark_1 == lily_pond_command_mark_2
