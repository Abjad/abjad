# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import NamedPitch


def test_NamedPitch___repr___01():
    r'''Named pitch repr is evaluable.
    '''

    named_pitch_1 = pitchtools.NamedPitch("cs''")
    named_pitch_2 = eval(repr(named_pitch_1))

    r'''
    NamedPitch("cs''")
    '''

    assert isinstance(named_pitch_1, pitchtools.NamedPitch)
    assert isinstance(named_pitch_2, pitchtools.NamedPitch)


def test_NamedPitch___repr___02():
    r'''Repr values.
    '''

    named_pitch = pitchtools.NamedPitch("cs''")

    assert repr(named_pitch) == 'NamedPitch("cs\'\'")'
    assert named_pitch._tools_package_qualified_repr == 'pitchtools.NamedPitch("cs\'\'")'
    assert named_pitch._tools_package_qualified_indented_repr == \
        named_pitch._tools_package_qualified_repr
