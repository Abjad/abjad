# -*- coding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_TonalAnalysisAgent_analyze_neighbor_notes_01():

    notes = scoretools.make_notes([0, 2, 4, 2, 0], [(1, 4)])
    staff = Staff(notes)

    selection = tonalanalysistools.select(staff[:])
    result = selection.analyze_neighbor_notes()
    result == [False, False, True, False, False]
