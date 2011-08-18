from abjad import *
import py.test


def test_LilyPondCommandMark___setattr___01():
    '''Slots constrain LilyPond command marks.
    '''

    lilypond_command_mark = marktools.LilyPondCommandMark('bar "||"')

    assert py.test.raises(AttributeError, "lilypond_command_mark.foo = 'bar'")

