# -*- encoding: utf-8 -*-
from abjad import *


def test_Inspector_detach_grace_containers_01():

    staff = Staff("c'8 d'8 e'8 f'8")

    grace_container = leaftools.GraceContainer(
        [Note("cs'16")], kind='grace')
    grace_container(staff[1])

    after_grace_container = leaftools.GraceContainer(
        [Note("ds'16")], kind='after')
    after_grace_container(staff[1])

    grace_containers = more(staff[1]).get_grace_containers()

    assert len(grace_containers) == 2

    assert grace_container in grace_containers
    assert after_grace_container in grace_containers

    grace_containers = more(staff[1]).detach_grace_containers()

    assert len(grace_containers) == 2

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )
