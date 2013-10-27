# -*- encoding: utf-8 -*-
from abjad import *


def test_mutationtools_AttributeInspectionAgent_get_grace_containers_01():

    staff = Staff("c'8 d'8 e'8 f'8")

    grace_container = containertools.GraceContainer(
        [Note("cs'16")], kind='grace')
    grace_container.attach(staff[1])

    after_grace_container = containertools.GraceContainer(
        [Note("ds'16")], kind='after')
    after_grace_container.attach(staff[1])

    grace_containers = inspect(staff[1]).get_grace_containers()

    assert len(grace_containers) == 2

    assert grace_container in grace_containers
    assert after_grace_container in grace_containers
