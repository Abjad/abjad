# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_InspectionAgent_get_grace_containers_01():

    staff = Staff("c'8 d'8 e'8 f'8")

    grace_container = scoretools.GraceContainer(
        [Note("cs'16")], kind='grace')
    attach(grace_container, staff[1])

    after_grace_container = scoretools.GraceContainer(
        [Note("ds'16")], kind='after')
    attach(after_grace_container, staff[1])

    grace_containers = inspect_(staff[1]).get_grace_containers()

    assert len(grace_containers) == 2

    assert grace_container in grace_containers
    assert after_grace_container in grace_containers
