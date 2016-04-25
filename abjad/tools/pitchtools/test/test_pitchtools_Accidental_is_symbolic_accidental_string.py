# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Accidental_is_symbolic_accidental_string_01():

    assert pitchtools.Accidental.is_symbolic_string('#')
    assert pitchtools.Accidental.is_symbolic_string('##')
    assert pitchtools.Accidental.is_symbolic_string('b')
    assert pitchtools.Accidental.is_symbolic_string('bb')
    assert pitchtools.Accidental.is_symbolic_string('+')
    assert pitchtools.Accidental.is_symbolic_string('#+')
    assert pitchtools.Accidental.is_symbolic_string('~')
    assert pitchtools.Accidental.is_symbolic_string('b~')
    assert pitchtools.Accidental.is_symbolic_string('')


def test_pitchtools_Accidental_is_symbolic_accidental_string_02():

    assert not pitchtools.Accidental.is_symbolic_string('foo')
    assert not pitchtools.Accidental.is_symbolic_string(7)
    assert not pitchtools.Accidental.is_symbolic_string(True)
    assert not pitchtools.Accidental.is_symbolic_string('++')
    assert not pitchtools.Accidental.is_symbolic_string('~~')
