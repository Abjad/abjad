# -*- encoding: utf-8 -*-
from abjad import *


def test_TempoMark___eq___01():
    r'''Tempo indications compare equal when duration and mark match.
    '''

    t1 = Tempo(Duration(3, 32), 52)
    t2 = Tempo(Duration(3, 32), 52)
    assert t1 == t2


def test_TempoMark___eq___02():
    r'''Tempo indications do not compare equal
    when mathematically equal.
    '''

    t1 = Tempo(Duration(3, 32), 52)
    t2 = Tempo(Duration(6, 32), 104)
    assert not t1 == t2


def test_TempoMark___eq___03():
    r'''Tempo indications also compare textual indications.
    '''

    t1 = Tempo('Langsam', Duration(3, 32), 52)
    t2 = Tempo('Langsam', Duration(3, 32), 52)
    assert t1 == t2

    t1.textual_indication = 'Slow'
    assert not t1 == t2
