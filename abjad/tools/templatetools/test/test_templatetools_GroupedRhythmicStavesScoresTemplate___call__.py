# -*- coding: utf-8 -*-
from abjad import *


def test_templatetools_GroupedRhythmicStavesScoresTemplate___call___01():

    template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score = template()

    assert format(score) == stringtools.normalize(
        r'''
        \context Score = "Grouped Rhythmic Staves Score" <<
            \context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
                \context RhythmicStaff = "Staff 1" {
                    \context Voice = "Voice 1" {
                    }
                }
                \context RhythmicStaff = "Staff 2" {
                    \context Voice = "Voice 2" {
                    }
                }
                \context RhythmicStaff = "Staff 3" {
                    \context Voice = "Voice 3" {
                    }
                }
                \context RhythmicStaff = "Staff 4" {
                    \context Voice = "Voice 4" {
                    }
                }
            >>
        >>
        '''
        )


def test_templatetools_GroupedRhythmicStavesScoresTemplate___call___02():

    template = templatetools.GroupedRhythmicStavesScoreTemplate(staff_count=[2, 1, 2])
    score = template()

    assert format(score) == stringtools.normalize(
        r'''
        \context Score = "Grouped Rhythmic Staves Score" <<
            \context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
                \context RhythmicStaff = "Staff 1" <<
                    \context Voice = "Voice 1-1" {
                    }
                    \context Voice = "Voice 1-2" {
                    }
                >>
                \context RhythmicStaff = "Staff 2" {
                    \context Voice = "Voice 2" {
                    }
                }
                \context RhythmicStaff = "Staff 3" <<
                    \context Voice = "Voice 3-1" {
                    }
                    \context Voice = "Voice 3-2" {
                    }
                >>
            >>
        >>
        '''
        )
