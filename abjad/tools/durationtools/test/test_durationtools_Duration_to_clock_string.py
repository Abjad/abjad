# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_durationtools_Duration_to_clock_string_01():

    assert Duration(0).to_clock_string() == "0'00\""
    assert Duration(4).to_clock_string() == "0'04\""
    assert Duration(20).to_clock_string() == "0'20\""
    assert Duration(60).to_clock_string() == "1'00\""
    assert Duration(120).to_clock_string() == "2'00\""
    assert Duration(240).to_clock_string() == "4'00\""


def test_durationtools_Duration_to_clock_string_02():

    assert Duration(Fraction(0)).to_clock_string() == "0'00\""
    assert Duration(Fraction(3, 2)).to_clock_string() == "0'01\""
    assert Duration(Fraction(89, 14)).to_clock_string() == "0'06\""
    assert Duration(Fraction(116, 19)).to_clock_string() == "0'06\""
    assert Duration(Fraction(140, 3)).to_clock_string() == "0'46\""
    assert Duration(Fraction(180, 3)).to_clock_string() == "1'00\""


def test_durationtools_Duration_to_clock_string_03():

    assert pytest.raises(ValueError, 'Duration(-1.5).to_clock_string()')


def test_durationtools_Duration_to_clock_string_04():

    assert Duration(0).to_clock_string(escape_ticks=True) == "0'00\\\""
    assert Duration(4).to_clock_string(escape_ticks=True) == "0'04\\\""
    assert Duration(20).to_clock_string(escape_ticks=True) == "0'20\\\""
    assert Duration(60).to_clock_string(escape_ticks=True) == "1'00\\\""
    assert Duration(120).to_clock_string(escape_ticks=True) == "2'00\\\""
    assert Duration(240).to_clock_string(escape_ticks=True) == "4'00\\\""
