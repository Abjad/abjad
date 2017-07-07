# -*- coding: utf-8 -*-
import copy
from abjad import *


def test_scoretools_GraceContainer___copy___01():

    grace_container_1 = AfterGraceContainer([Note("d'32")])
    grace_container_2 = copy.copy(grace_container_1)

    assert grace_container_1 is not grace_container_2
    assert isinstance(grace_container_2, AfterGraceContainer)
