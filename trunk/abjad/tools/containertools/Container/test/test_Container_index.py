from abjad import *


def test_Container_index_01():
    '''Elements that compare equal return different indices in container.
    '''

    container = Container(4 * Note("c'4"))

    assert container.index(container[0]) == 0
    assert container.index(container[1]) == 1
    assert container.index(container[2]) == 2
    assert container.index(container[3]) == 3
