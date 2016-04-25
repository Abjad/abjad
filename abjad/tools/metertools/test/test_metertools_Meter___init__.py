# -*- coding: utf-8 -*-
from abjad import *


def test_metertools_Meter___init___01():

    time_signature = TimeSignature((2, 4))
    assert metertools.Meter(time_signature).rtm_format == \
        '(2/4 (1/4 1/4))'


def test_metertools_Meter___init___02():

    time_signature = TimeSignature((3, 4))
    assert metertools.Meter(time_signature).rtm_format == \
        '(3/4 (1/4 1/4 1/4))'


def test_metertools_Meter___init___03():

    time_signature = TimeSignature((4, 4))
    assert metertools.Meter(time_signature).rtm_format == \
        '(4/4 (1/4 1/4 1/4 1/4))'


def test_metertools_Meter___init___04():

    time_signature = TimeSignature((6, 8))
    assert metertools.Meter(time_signature).rtm_format == \
        '(6/8 ((3/8 (1/8 1/8 1/8)) (3/8 (1/8 1/8 1/8))))'


def test_metertools_Meter___init___05():

    time_signature = TimeSignature((5, 8))
    assert metertools.Meter(time_signature).rtm_format == \
        '(5/8 ((3/8 (1/8 1/8 1/8)) (2/8 (1/8 1/8))))'


def test_metertools_Meter___init___06():

    time_signature = TimeSignature((12, 4))
    assert metertools.Meter(time_signature).rtm_format == \
        '(12/4 ((3/4 (1/4 1/4 1/4)) (3/4 (1/4 1/4 1/4)) (3/4 (1/4 1/4 1/4)) (3/4 (1/4 1/4 1/4))))'


def test_metertools_Meter___init___07():

    time_signature = TimeSignature((1, 4))
    assert metertools.Meter(time_signature).rtm_format == \
        '(1/4 (1/4))'


def test_metertools_Meter___init___08():

    time_signature = TimeSignature((10, 4))
    assert metertools.Meter(time_signature).rtm_format == \
        '(10/4 ((5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)))) (5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))))'

def test_metertools_Meter___init___09():

    time_signature = TimeSignature((11, 4))
    assert metertools.Meter(time_signature).rtm_format == \
        '(11/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'


def test_metertools_Meter___init___10():

    hierarchy = metertools.Meter('(4/4 ((2/4 (1/4 1/4)) (2/4 (1/4 1/4))))')
