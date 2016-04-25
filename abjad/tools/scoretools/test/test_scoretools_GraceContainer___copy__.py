# -*- coding: utf-8 -*-
import copy
from abjad import *


def test_scoretools_GraceContainer___copy___01():
    r'''Grace containers copy kind.
    '''

    grace_container_1 = scoretools.GraceContainer([Note("d'32")], kind='after')
    grace_container_2 = copy.copy(grace_container_1)

    assert grace_container_1 is not grace_container_2
    assert grace_container_1.kind == grace_container_2.kind == 'after'
