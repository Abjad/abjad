import abjad
import pytest


def test_scoretools_Component__get_in_my_logical_voice_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")

    assert staff[0]._get_in_my_logical_voice(0, abjad.Note) is staff[0]
    assert staff[0]._get_in_my_logical_voice(1, abjad.Note) is staff[1]
    assert staff[0]._get_in_my_logical_voice(2, abjad.Note) is staff[2]
    assert staff[0]._get_in_my_logical_voice(3, abjad.Note) is staff[3]

    assert staff[3]._get_in_my_logical_voice(0, abjad.Note) is staff[3]
    assert staff[3]._get_in_my_logical_voice(-1, abjad.Note) is staff[2]
    assert staff[3]._get_in_my_logical_voice(-2, abjad.Note) is staff[1]
    assert staff[3]._get_in_my_logical_voice(-3, abjad.Note) is staff[0]


def test_scoretools_Component__get_in_my_logical_voice_02():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")

    assert staff[0]._get_in_my_logical_voice(99, abjad.Note) is None


def test_scoretools_Component__get_in_my_logical_voice_03():
    r'''Different anonymous contexts create different logical voices.
    '''

    container = abjad.Container([abjad.Voice("c'8 d'8"), abjad.Voice("e'8 f'8")])
    leaves = abjad.select(container).leaves()

    assert leaves[0]._get_in_my_logical_voice(1, abjad.Note) is leaves[1]
    assert leaves[1]._get_in_my_logical_voice(1, abjad.Note) is None
    assert leaves[2]._get_in_my_logical_voice(1, abjad.Note) is leaves[3]
    assert container[0]._get_in_my_logical_voice(1, abjad.Voice) is None


def test_scoretools_Component__get_in_my_logical_voice_04():
    r'''Differently named contexts create different logical voices.
    '''

    container = abjad.Container([abjad.Voice("c'8 d'8"), abjad.Voice("e'8 f'8")])
    container[0].name = 'voice'
    leaves = abjad.select(container).leaves()

    assert container[0]._get_in_my_logical_voice(1, abjad.Voice) is None
    assert leaves[0]._get_in_my_logical_voice(1, abjad.Note) is leaves[1]
    assert leaves[1]._get_in_my_logical_voice(1, abjad.Note) is None
    assert leaves[2]._get_in_my_logical_voice(1, abjad.Note) is leaves[3]


def test_scoretools_Component__get_in_my_logical_voice_05():
    r'''Like-named contexts create the same logical voice.
    '''

    container = abjad.Container([abjad.Voice("c'8 d'8"), abjad.Voice("e'8 f'8")])
    container[0].name = 'voice'
    container[1].name = 'voice'
    leaves = abjad.select(container).leaves()

    assert container[0]._get_in_my_logical_voice(1, abjad.Voice) is container[1]
    assert container[1]._get_in_my_logical_voice(1, abjad.Voice) is None
    assert leaves[1]._get_in_my_logical_voice(1, abjad.Note) is leaves[2]


def test_scoretools_Component__get_in_my_logical_voice_06():
    r'''Like-named contexts create the same logical voice.
    The intervening rest exists in a different logical voice.
    '''

    container = abjad.Container([abjad.Voice("c'8 d'8"), abjad.Rest('r2'), abjad.Voice("e'8 f'8")])
    container[0].name = 'voice'
    container[-1].name = 'voice'
    leaves = abjad.select(container).leaves()

    assert container[0]._get_in_my_logical_voice(1, abjad.Voice) is container[2]
    assert leaves[1]._get_in_my_logical_voice(1, abjad.Note) is leaves[3]


def test_scoretools_Component__get_in_my_logical_voice_07():
    r'''Get component in same logical voice across simultaneous containers.
    '''

    container_1 = abjad.Container([abjad.Voice("c''8 d''8"), abjad.Voice("c'8 d'8")])
    container_1[0].name = 'voiceOne'
    container_1[1].name = 'voiceTwo'
    container_1.is_simultaneous = True
    container_2 = abjad.Container([abjad.Voice("e''8 f''8"), abjad.Voice("e'8 f'8")])
    container_2[0].name = 'voiceOne'
    container_2[1].name = 'voiceTwo'
    container_2.is_simultaneous = True
    staff = abjad.Staff([container_1, container_2])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            <<
                \context Voice = "voiceOne" {
                    c''8
                    d''8
                }
                \context Voice = "voiceTwo" {
                    c'8
                    d'8
                }
            >>
            <<
                \context Voice = "voiceOne" {
                    e''8
                    f''8
                }
                \context Voice = "voiceTwo" {
                    e'8
                    f'8
                }
            >>
        }
        '''
        )

    assert container_1[0]._get_in_my_logical_voice(1, abjad.Voice) is container_2[0]
    assert container_1[1]._get_in_my_logical_voice(1, abjad.Voice) is container_2[1]
    assert container_1[0][1]._get_in_my_logical_voice(1, abjad.Note) is \
        container_2[0][0]
    assert container_1[1][1]._get_in_my_logical_voice(1, abjad.Note) is \
        container_2[1][0]
