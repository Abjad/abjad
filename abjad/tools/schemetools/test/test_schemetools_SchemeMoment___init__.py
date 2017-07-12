# -*- coding: utf-8 -*-
import abjad


def test_schemetools_SchemeMoment___init___01():
    r'''Initialize scheme moment from fraction.
    '''

    scheme_moment = abjad.SchemeMoment(abjad.Fraction(1, 68))
    assert format(scheme_moment) == '#(ly:make-moment 1 68)'


def test_schemetools_SchemeMoment___init___02():
    r'''Initialize scheme moment from integer.
    '''

    scheme_moment = abjad.SchemeMoment(1)
    assert format(scheme_moment) == '#(ly:make-moment 1 1)'


def test_schemetools_SchemeMoment___init___03():
    r'''Initialize scheme moment from integer pair.
    '''

    scheme_moment = abjad.SchemeMoment((1, 68))
    assert format(scheme_moment) == '#(ly:make-moment 1 68)'


def test_schemetools_SchemeMoment___init___04():
    r'''Initialize scheme moment from two positive integers.
    '''

    scheme_moment = abjad.SchemeMoment(1, 68)
    assert format(scheme_moment) == '#(ly:make-moment 1 68)'


def test_schemetools_SchemeMoment___init___05():
    r'''Initialize scheme moment from other scheme moment.
    '''

    scheme_moment_1 = abjad.SchemeMoment(abjad.Fraction(1, 68))
    scheme_moment_2 = abjad.SchemeMoment(scheme_moment_1)
    assert format(scheme_moment_1) == '#(ly:make-moment 1 68)'
    assert format(scheme_moment_2) == '#(ly:make-moment 1 68)'
    assert scheme_moment_1 is not scheme_moment_2
