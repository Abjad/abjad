# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_transpose_named_pitch_by_numbered_interval_and_respell_01():

    pitch = NamedPitch(0)

    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, 1, 0) == NamedPitch('dff', 4)
    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, 1, 0.5) == NamedPitch('dtqf', 4)
    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, 1, 1) == NamedPitch('df', 4)
    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, 1, 1.5) == NamedPitch('dqf', 4)
    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, 1, 2) == NamedPitch('d', 4)
    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, 1, 2.5) == NamedPitch('dqs', 4)
    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, 1, 3) == NamedPitch('ds', 4)
    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, 1, 3.5) == NamedPitch('dtqs', 4)
    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, 1, 4) == NamedPitch('dss', 4)

    statement = 'pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, 1, 4.5)'
    assert pytest.raises(KeyError, statement)


def test_pitchtools_transpose_named_pitch_by_numbered_interval_and_respell_02():

    pitch = NamedPitch(0)

    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, -1, 0) == NamedPitch('bs', 3)
    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, -1, -0.5) == NamedPitch('bqs', 3)
    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, -1, -1) == NamedPitch('b', 3)
    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, -1, -1.5) == NamedPitch('bqf', 3)
    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, -1, -2) == NamedPitch('bf', 3)
    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, -1, -2.5) == NamedPitch('btqf', 3)
    assert pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(pitch, -1, -3) == NamedPitch('bff', 3)
