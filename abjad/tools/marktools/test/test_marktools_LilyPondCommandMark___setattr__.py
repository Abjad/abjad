# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_marktools_LilyPondCommandMark___setattr___01():
    r'''Slots constrain LilyPond command marks.
    '''

    lilypond_command_mark = marktools.LilyPondCommandMark('break')

    assert pytest.raises(AttributeError, "lilypond_command_mark.foo = 'bar'")
