import abjad


def test_Meter___init___01():
    rtc = abjad.rhythmtrees.RhythmTreeContainer((2, 4))
    assert abjad.Meter(rtc).rtm_format == "(2/4 (1/4 1/4))"


def test_Meter___init___02():
    rtc = abjad.rhythmtrees.RhythmTreeContainer((3, 4))
    assert abjad.Meter(rtc).rtm_format == "(3/4 (1/4 1/4 1/4))"


def test_Meter___init___03():
    rtc = abjad.rhythmtrees.RhythmTreeContainer((4, 4))
    assert abjad.Meter(rtc).rtm_format == "(4/4 (1/4 1/4 1/4 1/4))"


def test_Meter___init___04():
    rtc = abjad.rhythmtrees.RhythmTreeContainer((6, 8))
    string = "(6/8 ((3/8 (1/8 1/8 1/8)) (3/8 (1/8 1/8 1/8))))"
    assert abjad.Meter(rtc).rtm_format == string


def test_Meter___init___05():
    rtc = abjad.rhythmtrees.RhythmTreeContainer((5, 8))
    string = "(5/8 ((3/8 (1/8 1/8 1/8)) (2/8 (1/8 1/8))))"
    assert abjad.Meter(rtc).rtm_format == string


def test_Meter___init___06():
    rtc = abjad.rhythmtrees.RhythmTreeContainer((12, 4))
    string = "(12/4 ((3/4 (1/4 1/4 1/4)) (3/4 (1/4 1/4 1/4))"
    string += " (3/4 (1/4 1/4 1/4)) (3/4 (1/4 1/4 1/4))))"
    abjad.Meter(rtc).rtm_format == string


def test_Meter___init___07():
    rtc = abjad.rhythmtrees.RhythmTreeContainer((1, 4))
    assert abjad.Meter(rtc).rtm_format == "(1/4 (1/4))"


def test_Meter___init___08():
    rtc = abjad.rhythmtrees.RhythmTreeContainer((10, 4))
    string = "(10/4 ((5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))"
    string += " (5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))))"
    assert abjad.Meter(rtc).rtm_format == string


def test_Meter___init___09():
    rtc = abjad.rhythmtrees.RhythmTreeContainer((11, 4))
    string = "(11/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4))"
    string += " (2/4 (1/4 1/4)) (2/4 (1/4 1/4))))"
    assert abjad.Meter(rtc).rtm_format == string


def test_Meter___iter___01():
    rtc = abjad.rhythmtrees.RhythmTreeContainer((3, 8))
    meter = abjad.Meter(rtc)
    pairs = [pair for pair in meter]
    assert pairs == [
        ((0, 8), (1, 8)),
        ((1, 8), (2, 8)),
        ((2, 8), (3, 8)),
        ((0, 8), (3, 8)),
    ]
