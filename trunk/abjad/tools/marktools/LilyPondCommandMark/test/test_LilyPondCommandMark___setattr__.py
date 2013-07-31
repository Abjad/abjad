# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_LilyPondCommandMark___setattr___01():
    r'''Slots constrain LilyPond command marks.
    '''

    lilypond_command_mark = marktools.LilyPondCommandMark('break')

    assert py.test.raises(AttributeError, "lilypond_command_mark.foo = 'bar'")
