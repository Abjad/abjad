from abjad import *
from abjad.tools import rhythmtreetools


def test_RhythmTreeNode___call___01():

    rtm = '(1 (1 1 1 1))'
    tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
    result = tree((1, 4))

    assert isinstance(result, list)
    assert len(result) == 4
    assert all([isinstance(x, Note) for x in result])
    assert all([x.written_duration == Duration(1, 16) for x in result])


def test_RhythmTreeNode___call___02():

    rtm = '(1 (1 (2 (1 1 1)) 2))'
    tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
    result = tree((1, 4))

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], tuplettools.FixedDurationTuplet)
    assert result[0].lilypond_format == "\\times 4/5 {\n\tc'16\n\t\\times 2/3 {\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t}\n\tc'8\n}"


def test_RhythmTreeNode___call___03():

    rtm = '(1 (1 (2 (1 (2 (1 1)) 1)) 2))'
    tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
    result = tree((1, 4))

    assert result[0].lilypond_format == "\\times 4/5 {\n\tc'16\n\tc'32\n\tc'32\n\tc'32\n\tc'32\n\tc'8\n}"

