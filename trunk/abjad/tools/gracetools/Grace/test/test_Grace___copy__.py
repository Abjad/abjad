from abjad import *
import copy


def test_Grace___copy___01():
    '''Grace containers copy kind.
    '''

    grace_container_1 = gracetools.Grace([Note("d'32")], kind = 'after')
    grace_container_2 = copy.copy(grace_container_1)

    assert grace_container_1 is not grace_container_2
    assert grace_container_1.kind == grace_container_2.kind == 'after'
