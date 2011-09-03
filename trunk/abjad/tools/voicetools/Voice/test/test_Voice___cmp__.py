from abjad import *
import py.test


def test_Voice___cmp___01():
    '''Compare voice to itself.
    '''

    voice = Voice([])

    assert voice == voice
    assert not voice != voice

    comparison_string = 'voice <  voice'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'voice <= voice'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'voice >  voice'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'voice >= voice'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Voice___cmp___02():
    '''Compare voices.
    '''

    voice_1 = Voice([])
    voice_2 = Voice([])

    assert not voice_1 == voice_2
    assert      voice_1 != voice_2

    comparison_string = 'voice_1 <  voice_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'voice_1 <= voice_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'voice_1 >  voice_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'voice_1 >= voice_2'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Voice___cmp___03():
    '''Compare voice to foreign type.
    '''

    voice = Voice([])

    assert not voice == 'foo'
    assert      voice != 'foo'

    comparison_string = "voice <  'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "voice <= 'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "voice >  'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = "voice >= 'foo'"
    assert py.test.raises(NotImplementedError, comparison_string)
