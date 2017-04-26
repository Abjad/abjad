# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import Registration
from abjad.tools.pitchtools import RegistrationList


def test_pitchtools_RegistrationList___repr___01():

    registrations_1 = pitchtools.RegistrationList([[('[A0, C8]', -18)]])
    registrations_2 = eval(repr(registrations_1))

    assert isinstance(registrations_1, pitchtools.RegistrationList)
    assert isinstance(registrations_2, pitchtools.RegistrationList)
    assert registrations_1 == registrations_2
