# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.indicatortools import LilyPondCommand


def test_indicatortools_LilyPondCommand___repr___01():
    r'''Repr of unattached LilyPond command is evaluable.
    '''

    lily_pond_command_1 = indicatortools.LilyPondCommand('break')
    lily_pond_command_2 = eval(repr(lily_pond_command_1))

    assert isinstance(lily_pond_command_1, indicatortools.LilyPondCommand)
    assert isinstance(lily_pond_command_2, indicatortools.LilyPondCommand)
    assert lily_pond_command_1 == lily_pond_command_2
