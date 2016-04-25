# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Registration___init___01():
    r'''Initialize from items.
    '''

    mapping = pitchtools.Registration([('[A0, C4)', 15), ('[C4, C8)', 27)])
    assert isinstance(mapping, pitchtools.Registration)


def test_pitchtools_Registration___init___02():
    r'''Initialize from instance.
    '''

    mapping_1 = pitchtools.Registration([('[A0, C4)', 15), ('[C4, C8)', 27)])
    mapping_2 = pitchtools.Registration(mapping_1)

    assert isinstance(mapping_1, pitchtools.Registration)
    assert isinstance(mapping_2, pitchtools.Registration)
    assert mapping_1 == mapping_2


def test_pitchtools_Registration___init___03():
    r'''Initialize from named instance.
    '''

    mapping_1 = pitchtools.Registration(
        [('[A0, C4)', 15), ('[C4, C8)', 27)],
        )
    mapping_2 = pitchtools.Registration(mapping_1)

    assert isinstance(mapping_1, pitchtools.Registration)
    assert isinstance(mapping_2, pitchtools.Registration)
    assert mapping_1 == mapping_2


def test_pitchtools_Registration___init___04():
    r'''Initializeempty.
    '''

    mapping = pitchtools.Registration()
    assert isinstance(mapping, pitchtools.Registration)

    mapping = pitchtools.Registration([])
    assert isinstance(mapping, pitchtools.Registration)
