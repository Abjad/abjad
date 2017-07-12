# -*- coding: utf-8 -*-
import abjad
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_TonalAnalysisAgent_are_stepwise_ascending_notes_01():

    notes = [abjad.Note("c'8"), abjad.Note("d'8"), abjad.Note("e'8"), abjad.Note("f'8")]
    selection = abjad.analyze(notes)
    assert selection.are_stepwise_ascending_notes()


def test_tonalanalysistools_TonalAnalysisAgent_are_stepwise_ascending_notes_02():

    notes = [abjad.Note("c'8"), abjad.Note("d'8"), abjad.Note("e'8"), abjad.Note("f'8")]
    notes.reverse()
    selection = abjad.analyze(notes)
    assert not selection.are_stepwise_ascending_notes()
