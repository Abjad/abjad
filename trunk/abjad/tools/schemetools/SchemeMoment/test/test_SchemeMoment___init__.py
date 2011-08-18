from abjad import *


def test_SchemeMoment___init___01():
    '''Initialize scheme moment from fraction.
    '''

    scheme_moment = schemetools.SchemeMoment(Fraction(1, 68))
    assert scheme_moment.format == '#(ly:make-moment 1 68)'


def test_SchemeMoment___init___02():
    '''Initialize scheme moment from integer.
    '''

    scheme_moment = schemetools.SchemeMoment(1)
    assert scheme_moment.format == '#(ly:make-moment 1 1)'


def test_SchemeMoment___init___03():
    '''Initialize scheme moment from integer pair.
    '''

    scheme_moment = schemetools.SchemeMoment((1, 68))
    assert scheme_moment.format == '#(ly:make-moment 1 68)'


def test_SchemeMoment___init___04():
    '''Initialize scheme moment from two positive integers.
    '''

    scheme_moment = schemetools.SchemeMoment(1, 68)
    assert scheme_moment.format == '#(ly:make-moment 1 68)'


def test_SchemeMoment___init___05():
    '''Initialize scheme moment from other scheme moment.
    '''

    scheme_moment_1 = schemetools.SchemeMoment(Fraction(1, 68))
    scheme_moment_2 = schemetools.SchemeMoment(scheme_moment_1)
    assert scheme_moment_1.format == '#(ly:make-moment 1 68)'
    assert scheme_moment_2.format == '#(ly:make-moment 1 68)'
    assert scheme_moment_1 is not scheme_moment_2
