from abjad import *
from experimental import *


def test_BeatHierarchy___init___01():

    time_signature = contexttools.TimeSignatureMark((2, 4))
    assert quantizationtools.BeatHierarchy(time_signature).rtm_format == \
        '(2 (1 1))'


def test_BeatHierarchy___init___02():

    time_signature = contexttools.TimeSignatureMark((3, 4))
    assert quantizationtools.BeatHierarchy(time_signature).rtm_format == \
        '(3 (1 1 1))'


def test_BeatHierarchy___init___03():

    time_signature = contexttools.TimeSignatureMark((4, 4))
    assert quantizationtools.BeatHierarchy(time_signature).rtm_format == \
        '(4 ((2 (1 1)) (2 (1 1))))'


def test_BeatHierarchy___init___04():

    time_signature = contexttools.TimeSignatureMark((6, 8))
    assert quantizationtools.BeatHierarchy(time_signature).rtm_format == \
        '(6 ((3 (1 1 1)) (3 (1 1 1))))'


def test_BeatHierarchy___init___05():

    time_signature = contexttools.TimeSignatureMark((5, 8))
    assert quantizationtools.BeatHierarchy(time_signature).rtm_format == \
        '(5 ((3 (1 1 1)) (2 (1 1))))'


def test_BeatHierarchy___init___06():

    time_signature = contexttools.TimeSignatureMark((12, 4))
    assert quantizationtools.BeatHierarchy(time_signature).rtm_format == \
        '(12 ((6 ((3 (1 1 1)) (3 (1 1 1)))) (6 ((3 (1 1 1)) (3 (1 1 1))))))'


def test_BeatHierarchy___init___07():

    time_signature = contexttools.TimeSignatureMark((1, 4))
    assert quantizationtools.BeatHierarchy(time_signature).rtm_format == \
        '(1 (1))'


def test_BeatHierarchy___init___08():

    time_signature = contexttools.TimeSignatureMark((10, 4))
    assert quantizationtools.BeatHierarchy(time_signature).rtm_format == \
        '(10 ((5 ((3 (1 1 1)) (2 (1 1)))) (5 ((3 (1 1 1)) (2 (1 1))))))'


def test_BeatHierarchy___init___09():

    time_signature = contexttools.TimeSignatureMark((11, 4))
    assert quantizationtools.BeatHierarchy(time_signature).rtm_format == \
        '(11 ((3 (1 1 1)) (2 (1 1)) (2 (1 1)) (2 (1 1)) (2 (1 1))))'


def test_BeatHierarchy___init___10():

    time_signature = contexttools.TimeSignatureMark((25, 4))
    assert quantizationtools.BeatHierarchy(time_signature).rtm_format == \
        '(25 ((15 ((5 ((3 (1 1 1)) (2 (1 1)))) (5 ((3 (1 1 1)) (2 (1 1)))) (5 ((3 (1 1 1)) (2 (1 1)))))) (10 ((5 ((3 (1 1 1)) (2 (1 1)))) (5 ((3 (1 1 1)) (2 (1 1))))))))'
