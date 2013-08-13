# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Component__get_in_my_logical_voice_01():

    staff = Staff("c'8 d'8 e'8 f'8")

    assert staff[0]._get_in_my_logical_voice(0, Note) is staff[0]
    assert staff[0]._get_in_my_logical_voice(1, Note) is staff[1]
    assert staff[0]._get_in_my_logical_voice(2, Note) is staff[2]
    assert staff[0]._get_in_my_logical_voice(3, Note) is staff[3]

    assert staff[3]._get_in_my_logical_voice(0, Note) is staff[3]
    assert staff[3]._get_in_my_logical_voice(-1, Note) is staff[2]
    assert staff[3]._get_in_my_logical_voice(-2, Note) is staff[1]
    assert staff[3]._get_in_my_logical_voice(-3, Note) is staff[0]


def test_Component__get_in_my_logical_voice_02():

    staff = Staff("c'8 d'8 e'8 f'8")

    assert staff[0]._get_in_my_logical_voice(99, Note) is None


def test_Component__get_in_my_logical_voice_03():
    r'''Leaves within different anonymous parents have different
    parentage signatures and thus have no next namesake.
    '''

    container = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
    leaves = container.select_leaves()


    assert leaves[0]._get_in_my_logical_voice(1, Note) is leaves[1]
    assert leaves[1]._get_in_my_logical_voice(1, Note) is None
    assert leaves[2]._get_in_my_logical_voice(1, Note) is leaves[3]


def test_Component__get_in_my_logical_voice_04():
    r'''Anonymous containers with the same parentage structure have
    different parentage signatures and thus have no next namesake.
    '''

    container = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])

    assert container[0]._get_in_my_logical_voice(1, Voice) is None


def test_Component__get_in_my_logical_voice_05():
    r'''Differently named containers have different parentage signatures
    and thus have no next namesake.
    '''

    container = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
    container[0].name = 'voice'
    leaves = container.select_leaves()

    assert container[0]._get_in_my_logical_voice(1, Voice) is None
    assert leaves[0]._get_in_my_logical_voice(1, Note) is leaves[1]
    assert leaves[1]._get_in_my_logical_voice(1, Note) is None
    assert leaves[2]._get_in_my_logical_voice(1, Note) is leaves[3]


def test_Component__get_in_my_logical_voice_06():
    r'''Getting next namesake from a named component when another component
    with the same type and name exists after the caller returns the first
    next namesake found.
    '''

    container = Container([Voice("c'8 d'8"), Voice("e'8 f'8")])
    container[0].name = 'voice'
    container[1].name = 'voice'
    leaves = container.select_leaves()

    assert container[0]._get_in_my_logical_voice(1, Voice) is container[1]
    assert container[1]._get_in_my_logical_voice(1, Voice) is None
    assert leaves[1]._get_in_my_logical_voice(1, Note) is leaves[2]


def test_Component__get_in_my_logical_voice_07():
    r'''Components need not be strictly contiguous.
    '''

    container = Container([Voice("c'8 d'8"), Rest('r2'), Voice("e'8 f'8")])
    container[0].name = 'voice'
    container[-1].name = 'voice'
    leaves = container.select_leaves()

    assert container[0]._get_in_my_logical_voice(1, Voice) is container[2]
    assert leaves[1]._get_in_my_logical_voice(1, Note) is leaves[3]


def test_Component__get_in_my_logical_voice_08():
    r'''Get namesake across simultaneous containers.
    '''

    container_1 = Container([Voice("c''8 d''8"), Voice("c'8 d'8")])
    container_1[0].name = 'voiceOne'
    container_1[1].name = 'voiceTwo'
    container_1.is_simultaneous = True
    container_2 = Container([Voice("e''8 f''8"), Voice("e'8 f'8")])
    container_2[0].name = 'voiceOne'
    container_2[1].name = 'voiceTwo'
    container_2.is_simultaneous = True
    staff = Staff([container_1, container_2])

    assert testtools.compare(
        staff,
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

    assert container_1[0]._get_in_my_logical_voice(1, Voice) is container_2[0]
    assert container_1[1]._get_in_my_logical_voice(1, Voice) is container_2[1]
    assert container_1[0][1]._get_in_my_logical_voice(1, Note) is \
        container_2[0][0]
    assert container_1[1][1]._get_in_my_logical_voice(1, Note) is \
        container_2[1][0]
