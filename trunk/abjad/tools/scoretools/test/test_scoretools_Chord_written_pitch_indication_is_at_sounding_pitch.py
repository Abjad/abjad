# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_scoretools_Chord_written_pitch_indication_is_at_sounding_pitch_01():

    chord = Chord("<c' e' g'>4")

    assert chord.written_pitch_indication_is_at_sounding_pitch


def test_scoretools_Chord_written_pitch_indication_is_at_sounding_pitch_02():

    chord = Chord("<c' e' g'>4")
    chord.written_pitch_indication_is_at_sounding_pitch = False

    assert not chord.written_pitch_indication_is_at_sounding_pitch


def test_scoretools_Chord_written_pitch_indication_is_at_sounding_pitch_03():

    chord = Chord("<c' e' g'>4")

    statement = "chord.written_pitch_indication_is_at_sounding_pitch = 'foo'"
    assert py.test.raises(Exception, statement)
