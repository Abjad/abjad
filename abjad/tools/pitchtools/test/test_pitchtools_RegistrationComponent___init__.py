# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_RegistrationComponent___init___01():
    r'''Initialize from range and start pitch.
    '''

    component = pitchtools.RegistrationComponent('[A0, C8]', 15)
    assert isinstance(component, pitchtools.RegistrationComponent)
