from abjad import *
import py


def test_FixedDurationContainer_format_01():

    container = containertools.FixedDurationContainer((3, 8), "c'8 d'8 e'8")
    assert container.lilypond_format == "{\n\tc'8\n\td'8\n\te'8\n}"


def test_FixedDurationContainer_format_02():

    container = containertools.FixedDurationContainer((3, 8), "c'8 d'8")
    assert py.test.raises(Exception, 'container.format')


def test_FixedDurationContainer_format_03():

    container = containertools.FixedDurationContainer((3, 8), "c'8 d'8 e'8 f'8")
    assert py.test.raises(Exception, 'container.format')
