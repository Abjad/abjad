# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_RegistrationList___contains___01():
    r'''Work with mappings.
    '''

    registrations = pitchtools.RegistrationList([[('[A0, C8]', -18)]])
    assert pitchtools.Registration([('[A0, C8]', -18)]) in registrations


def test_pitchtools_RegistrationList___contains___02():
    r'''Work with mapping items.
    '''

    registrations = pitchtools.RegistrationList([[('[A0, C8]', -18)]])
    assert [('[A0, C8]', -18)] in registrations
