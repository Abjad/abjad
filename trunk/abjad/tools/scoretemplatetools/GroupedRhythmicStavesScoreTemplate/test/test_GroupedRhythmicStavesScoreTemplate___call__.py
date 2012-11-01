from abjad import *


def test_GroupedRhythmicStavesScoreTemplate___call___01():

    template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
    score = template()

    assert score.lilypond_format == '\\context Score = "Grouped Rhythmic Staves Score" <<\n\t\\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<\n\t\t\\context RhythmicStaff = "Staff 1" {\n\t\t\t\\context Voice = "Voice 1" {\n\t\t\t}\n\t\t}\n\t\t\\context RhythmicStaff = "Staff 2" {\n\t\t\t\\context Voice = "Voice 2" {\n\t\t\t}\n\t\t}\n\t\t\\context RhythmicStaff = "Staff 3" {\n\t\t\t\\context Voice = "Voice 3" {\n\t\t\t}\n\t\t}\n\t\t\\context RhythmicStaff = "Staff 4" {\n\t\t\t\\context Voice = "Voice 4" {\n\t\t\t}\n\t\t}\n\t>>\n>>'


def test_GroupedRhythmicStavesScoreTemplate___call___02():

    template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=[2, 1, 2])
    score = template()

    assert score.lilypond_format == '\\context Score = "Grouped Rhythmic Staves Score" <<\n\t\\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<\n\t\t\\context RhythmicStaff = "Staff 1" <<\n\t\t\t\\context Voice = "Voice 1-1" {\n\t\t\t}\n\t\t\t\\context Voice = "Voice 1-2" {\n\t\t\t}\n\t\t>>\n\t\t\\context RhythmicStaff = "Staff 2" {\n\t\t\t\\context Voice = "Voice 2" {\n\t\t\t}\n\t\t}\n\t\t\\context RhythmicStaff = "Staff 3" <<\n\t\t\t\\context Voice = "Voice 3-1" {\n\t\t\t}\n\t\t\t\\context Voice = "Voice 3-2" {\n\t\t\t}\n\t\t>>\n\t>>\n>>'
