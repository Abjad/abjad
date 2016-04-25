# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRange___init___01():
    r'''Initializes stop-specified pitch range.
    '''

    range_ = pitchtools.PitchRange('[-39, +inf]')
    assert range_.range_string == '[A0, +inf]'

    range_ = pitchtools.PitchRange('(-39, +inf]')
    assert range_.range_string == '(A0, +inf]'


def test_pitchtools_PitchRange___init___02():
    r'''Initializes start-specified pitch range.
    '''

    range_ = pitchtools.PitchRange('[-inf, C8]')
    assert range_.range_string == '[-inf, C8]'

    range_ = pitchtools.PitchRange('[-inf, C8)')
    assert range_.range_string == '[-inf, C8)'


def test_pitchtools_PitchRange___init___03():
    r'''Initializes start- and stop-specified pitch range.
    '''

    range_ = pitchtools.PitchRange('[A0, C8]')
    assert range_.range_string == '[A0, C8]'


def test_pitchtools_PitchRange___init___04():
    r'''Initializes with numbers.
    '''

    range_ = pitchtools.PitchRange('[-39, 48]')
    assert range_.range_string == '[A0, C8]'
