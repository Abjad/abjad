from abjad import *


def test_contexttools_get_effective_dynamic_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.DynamicMark('f')(staff[2])

    r'''
    \new Staff {
        c'8
        d'8
        e'8 \f
        f'8
    }
    '''

    assert contexttools.get_effective_dynamic(staff) is None
    assert contexttools.get_effective_dynamic(staff[0]) is None
    assert contexttools.get_effective_dynamic(staff[1]) is None
    assert contexttools.get_effective_dynamic(staff[2]) == contexttools.DynamicMark('f')
    assert contexttools.get_effective_dynamic(staff[3]) == contexttools.DynamicMark('f')
