from abjad import *


def test_gracetools_detach_grace_containers_attached_to_leaf_01():

    staff = Staff("c'8 d'8 e'8 f'8")

    grace_container = gracetools.Grace([Note("cs'16")], kind = 'grace')
    grace_container(staff[1])

    after_grace_container = gracetools.Grace([Note("ds'16")], kind = 'after')
    after_grace_container(staff[1])

    grace_containers = gracetools.get_grace_containers_attached_to_leaf(staff[1])

    assert len(grace_containers) == 2

    assert grace_container in grace_containers
    assert after_grace_container in grace_containers

    grace_containers = gracetools.detach_grace_containers_attached_to_leaf(staff[1])

    assert len(grace_containers) == 2

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
