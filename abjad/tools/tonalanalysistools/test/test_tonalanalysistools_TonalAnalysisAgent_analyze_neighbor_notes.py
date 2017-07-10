# -*- coding: utf-8 -*-
import abjad


def test_tonalanalysistools_TonalAnalysisAgent_analyze_neighbor_notes_01():

    maker = abjad.NoteMaker()
    notes = maker([0, 2, 4, 2, 0], [(1, 4)])
    staff = abjad.Staff(notes)

    selection = abjad.analyze(staff[:])
    result = selection.analyze_neighbor_notes()
    result == [False, False, True, False, False]
