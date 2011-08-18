from abjad import *


def test_gracetools_get_grace_containers_attached_to_leaf_01():

    staff = Staff("c'8 d'8 e'8 f'8")

    grace_container = gracetools.Grace([Note("cs'16")], kind = 'grace')
    grace_container(staff[1])

    after_grace_container = gracetools.Grace([Note("ds'16")], kind = 'after')
    after_grace_container(staff[1])

    grace_containers = gracetools.get_grace_containers_attached_to_leaf(staff[1])

    assert len(grace_containers) == 2

    assert grace_container in grace_containers
    assert after_grace_container in grace_containers
