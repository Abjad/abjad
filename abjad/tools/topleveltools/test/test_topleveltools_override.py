# -*- coding: utf-8 -*-
import abjad


def test_topleveltools_override_01():

    note = abjad.Note("c'4")
    abjad.override(note).accidental.color = 'red'
    assert abjad.override(note).accidental.color == 'red'
