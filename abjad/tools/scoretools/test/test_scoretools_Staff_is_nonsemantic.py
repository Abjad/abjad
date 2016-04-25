# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Staff_is_nonsemantic_01():

    voice = Staff([])
    assert not voice.is_nonsemantic


def test_scoretools_Staff_is_nonsemantic_02():

    voice = Staff([])
    voice.is_nonsemantic = True

    assert voice.is_nonsemantic


def test_scoretools_Staff_is_nonsemantic_03():

    voice = Staff([])

    assert pytest.raises(TypeError, "voice.is_nonsemantic = 'foo'")
