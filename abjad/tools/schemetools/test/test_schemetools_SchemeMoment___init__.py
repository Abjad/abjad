# -*- coding: utf-8 -*-
from abjad import *


def test_schemetools_SchemeMoment___init___01():
    r'''Initialize scheme moment from fraction.
    '''

    scheme_moment = schemetools.SchemeMoment(Fraction(1, 68))
    assert format(scheme_moment) == '#(ly:make-moment 1 68)'


def test_schemetools_SchemeMoment___init___02():
    r'''Initialize scheme moment from integer.
    '''

    scheme_moment = schemetools.SchemeMoment(1)
    assert format(scheme_moment) == '#(ly:make-moment 1 1)'


def test_schemetools_SchemeMoment___init___03():
    r'''Initialize scheme moment from integer pair.
    '''

    scheme_moment = schemetools.SchemeMoment((1, 68))
    assert format(scheme_moment) == '#(ly:make-moment 1 68)'


def test_schemetools_SchemeMoment___init___04():
    r'''Initialize scheme moment from two positive integers.
    '''

    scheme_moment = schemetools.SchemeMoment(1, 68)
    assert format(scheme_moment) == '#(ly:make-moment 1 68)'


def test_schemetools_SchemeMoment___init___05():
    r'''Initialize scheme moment from other scheme moment.
    '''

    scheme_moment_1 = schemetools.SchemeMoment(Fraction(1, 68))
    scheme_moment_2 = schemetools.SchemeMoment(scheme_moment_1)
    assert format(scheme_moment_1) == '#(ly:make-moment 1 68)'
    assert format(scheme_moment_2) == '#(ly:make-moment 1 68)'
    assert scheme_moment_1 is not scheme_moment_2
