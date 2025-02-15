import abjad


def test_Meter___init___01():
    rtc = abjad.meter.make_best_guess_rtc((2, 4))
    assert abjad.Meter(rtc).rtm_format == "(2/4 (1/4 1/4))"


def test_Meter___init___02():
    rtc = abjad.meter.make_best_guess_rtc((3, 4))
    assert abjad.Meter(rtc).rtm_format == "(3/4 (1/4 1/4 1/4))"


def test_Meter___init___03():
    rtc = abjad.meter.make_best_guess_rtc((4, 4))
    assert abjad.Meter(rtc).rtm_format == "(4/4 (1/4 1/4 1/4 1/4))"


def test_Meter___init___04():
    rtc = abjad.meter.make_best_guess_rtc((6, 8))
    string = "(6/8 ((3/8 (1/8 1/8 1/8)) (3/8 (1/8 1/8 1/8))))"
    assert abjad.Meter(rtc).rtm_format == string


def test_Meter___init___05():
    rtc = abjad.meter.make_best_guess_rtc((5, 8))
    string = "(5/8 ((3/8 (1/8 1/8 1/8)) (2/8 (1/8 1/8))))"
    assert abjad.Meter(rtc).rtm_format == string


def test_Meter___init___06():
    rtc = abjad.meter.make_best_guess_rtc((12, 4))
    string = "(12/4 ((3/4 (1/4 1/4 1/4)) (3/4 (1/4 1/4 1/4))"
    string += " (3/4 (1/4 1/4 1/4)) (3/4 (1/4 1/4 1/4))))"
    abjad.Meter(rtc).rtm_format == string


def test_Meter___init___07():
    rtc = abjad.meter.make_best_guess_rtc((1, 4))
    assert abjad.Meter(rtc).rtm_format == "(1/4 (1/4))"


def test_Meter___init___08():
    rtc = abjad.meter.make_best_guess_rtc((10, 4))
    string = "(10/4 ((5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))"
    string += " (5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))))"
    assert abjad.Meter(rtc).rtm_format == string


def test_Meter___init___09():
    rtc = abjad.meter.make_best_guess_rtc((11, 4))
    string = "(11/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4))"
    string += " (2/4 (1/4 1/4)) (2/4 (1/4 1/4))))"
    assert abjad.Meter(rtc).rtm_format == string


def test_Meter___iter___01():
    rtc = abjad.meter.make_best_guess_rtc((3, 8))
    meter = abjad.Meter(rtc)
    pairs = [pair for pair in meter]
    assert pairs == [
        ((0, 8), (1, 8)),
        ((1, 8), (2, 8)),
        ((2, 8), (3, 8)),
        ((0, 8), (3, 8)),
    ]
