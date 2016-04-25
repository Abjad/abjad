# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Registration___contains___01():
    r'''Works with components.
    '''

    mapping = pitchtools.Registration([('[A0, C4)', 15), ('[C4, C8)', 27)])
    assert pitchtools.RegistrationComponent('[A0, C4)', 15) in mapping


def test_pitchtools_Registration___contains___02():
    r'''Works with component items.
    '''

    mapping = pitchtools.Registration([('[A0, C4)', 15), ('[C4, C8)', 27)])
    assert ('[A0, C4)', 15) in mapping
