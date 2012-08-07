from abjad import *


def test_RhythmTreeContainer___call___01():

    rtm = '(1 (1 (2 (1 1 1)) 2))'
    tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
    result = tree((1, 4))

    assert isinstance(result, list)
    assert len(result) == 1

    r'''
    \times 4/5 {
        c'16
        \times 2/3 {
            c'16
            c'16
            c'16
        }
        c'8
    }
    '''

    assert result[0].lilypond_format == "\\times 4/5 {\n\tc'16\n\t\\times 2/3 {\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t}\n\tc'8\n}"


def test_RhythmTreeContainer___call___02():

    rtm = '(1 (1 (2 (1 1 1 1)) 1))'
    tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
    result = tree((1, 4))

    assert isinstance(result, list)
    assert len(result) == 6
    assert [x.lilypond_format for x in result] == ["c'16", "c'32", "c'32", "c'32", "c'32", "c'16"]
