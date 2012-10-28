from abjad import *
# back-dependency to experimental branch is not allowed
#from experimental import *

import py
py.test.skip('back-dependency to experimental brach is now allowed')


def test_BeatHierarchy___init___01():

    time_signature = contexttools.TimeSignatureMark((2, 4))
    assert timesignaturetools.BeatHierarchy(time_signature).rtm_format == \
        '(2/4 (1/4 1/4))'


def test_BeatHierarchy___init___02():

    time_signature = contexttools.TimeSignatureMark((3, 4))
    assert timesignaturetools.BeatHierarchy(time_signature).rtm_format == \
        '(3/4 (1/4 1/4 1/4))'


def test_BeatHierarchy___init___03():

    time_signature = contexttools.TimeSignatureMark((4, 4))
    assert timesignaturetools.BeatHierarchy(time_signature).rtm_format == \
        '(4/4 ((2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'


def test_BeatHierarchy___init___04():

    time_signature = contexttools.TimeSignatureMark((6, 8))
    assert timesignaturetools.BeatHierarchy(time_signature).rtm_format == \
        '(6/8 ((3/8 (1/8 1/8 1/8)) (3/8 (1/8 1/8 1/8))))'


def test_BeatHierarchy___init___05():

    time_signature = contexttools.TimeSignatureMark((5, 8))
    assert timesignaturetools.BeatHierarchy(time_signature).rtm_format == \
        '(5/8 ((3/8 (1/8 1/8 1/8)) (2/8 (1/8 1/8))))'


def test_BeatHierarchy___init___06():

    time_signature = contexttools.TimeSignatureMark((12, 4))
    assert timesignaturetools.BeatHierarchy(time_signature).rtm_format == \
        '(12/4 ((6/4 ((3/4 (1/4 1/4 1/4)) (3/4 (1/4 1/4 1/4)))) (6/4 ((3/4 (1/4 1/4 1/4)) (3/4 (1/4 1/4 1/4))))))'


def test_BeatHierarchy___init___07():

    time_signature = contexttools.TimeSignatureMark((1, 4))
    assert timesignaturetools.BeatHierarchy(time_signature).rtm_format == \
        '(1/4 (1/4))'


def test_BeatHierarchy___init___08():

    time_signature = contexttools.TimeSignatureMark((10, 4))
    assert timesignaturetools.BeatHierarchy(time_signature).rtm_format == \
        '(10/4 ((5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)))) (5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))))'


def test_BeatHierarchy___init___09():

    time_signature = contexttools.TimeSignatureMark((11, 4))
    assert timesignaturetools.BeatHierarchy(time_signature).rtm_format == \
        '(11/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'


def test_BeatHierarchy___init___10():

    time_signature = contexttools.TimeSignatureMark((25, 4))
    assert timesignaturetools.BeatHierarchy(time_signature).rtm_format == \
        '(25/4 ((15/4 ((5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)))) (5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)))) (5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)))))) (10/4 ((5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)))) (5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))))))'
