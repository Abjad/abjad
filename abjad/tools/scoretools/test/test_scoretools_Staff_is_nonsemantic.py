# -*- encoding: utf-8 -*-
from abjad import *
import pytest


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
