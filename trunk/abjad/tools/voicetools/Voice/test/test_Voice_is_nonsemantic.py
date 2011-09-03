from abjad import *
import py.test


def test_Voice_is_nonsemantic_01():

    voice = Voice([])
    assert not voice.is_nonsemantic


def test_Voice_is_nonsemantic_02():

    voice = Voice([])
    voice.is_nonsemantic = True

    assert voice.is_nonsemantic


def test_Voice_is_nonsemantic_03():

    voice = Voice([])

    assert py.test.raises(TypeError, "voice.is_nonsemantic = 'foo'")
