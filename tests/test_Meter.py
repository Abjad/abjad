import abjad


def test_Meter___init___01():
    assert abjad.Meter((2, 4)).rtm_format == "(2/4 (1/4 1/4))"


def test_Meter___init___02():
    assert abjad.Meter((3, 4)).rtm_format == "(3/4 (1/4 1/4 1/4))"


def test_Meter___init___03():
    assert abjad.Meter((4, 4)).rtm_format == "(4/4 (1/4 1/4 1/4 1/4))"


def test_Meter___init___04():
    string = "(6/8 ((3/8 (1/8 1/8 1/8)) (3/8 (1/8 1/8 1/8))))"
    assert abjad.Meter((6, 8)).rtm_format == string


def test_Meter___init___05():
    string = "(5/8 ((3/8 (1/8 1/8 1/8)) (2/8 (1/8 1/8))))"
    assert abjad.Meter((5, 8)).rtm_format == string


def test_Meter___init___06():
    string = "(12/4 ((3/4 (1/4 1/4 1/4)) (3/4 (1/4 1/4 1/4))"
    string += " (3/4 (1/4 1/4 1/4)) (3/4 (1/4 1/4 1/4))))"
    abjad.Meter((12, 4)).rtm_format == string


def test_Meter___init___07():
    assert abjad.Meter((1, 4)).rtm_format == "(1/4 (1/4))"


def test_Meter___init___08():
    string = "(10/4 ((5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))"
    string += " (5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))))"
    assert abjad.Meter((10, 4)).rtm_format == string


def test_Meter___init___09():
    string = "(11/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4))"
    string += " (2/4 (1/4 1/4)) (2/4 (1/4 1/4))))"
    assert abjad.Meter((11, 4)).rtm_format == string


def test_Meter___iter___01():
    meter = abjad.Meter((3, 8))
    pairs = [pair for pair in meter]
    assert pairs == [
        ((0, 8), (1, 8)),
        ((1, 8), (2, 8)),
        ((2, 8), (3, 8)),
        ((0, 8), (3, 8)),
    ]
