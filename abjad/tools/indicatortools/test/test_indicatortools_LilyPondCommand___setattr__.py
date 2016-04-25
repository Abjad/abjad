# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_LilyPondCommand___setattr___01():
    r'''Slots constrain LilyPond commands.
    '''

    lilypond_command = indicatortools.LilyPondCommand('break')

    assert pytest.raises(AttributeError, "lilypond_command.foo = 'bar'")
