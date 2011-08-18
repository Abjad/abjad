from abjad import *


def test_Container__music___id___01():
    '''
    Container music lists are unique per instance,
    rather than shared between different instances.
    '''

    t1 = Container()
    t2 = Container()

    assert id(t1._music) != id(t2._music)
