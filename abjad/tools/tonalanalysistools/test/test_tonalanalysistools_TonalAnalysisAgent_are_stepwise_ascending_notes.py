# -*- coding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_TonalAnalysisAgent_are_stepwise_ascending_notes_01():

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    selection = tonalanalysistools.select(notes)
    assert selection.are_stepwise_ascending_notes()


def test_tonalanalysistools_TonalAnalysisAgent_are_stepwise_ascending_notes_02():

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    notes.reverse()
    selection = tonalanalysistools.select(notes)
    assert not selection.are_stepwise_ascending_notes()
