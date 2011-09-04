from abjad import *


def test_contexttools_get_effective_time_signature_01():
    '''The default effective meter is none.
    '''

    t = Staff("c'8 d'8 e'8 f'8")

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    for leaf in t:
        assert contexttools.get_effective_time_signature(leaf) is None


def test_contexttools_get_effective_time_signature_02():
    '''Forced meter settings propagate to later leaves.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    contexttools.TimeSignatureMark((2, 8))(t[0])

    r'''
    \new Staff {
        \time 2/8
        c'8
        d'8
        e'8
        f'8
    }
    '''

    for leaf in t:
        assert contexttools.get_effective_time_signature(leaf) == contexttools.TimeSignatureMark((2, 8))


def test_contexttools_get_effective_time_signature_03():
    '''Setting and then clearing works as expected.'''

    t = Staff("c'8 d'8 e'8 f'8")
    time_signature = contexttools.TimeSignatureMark((2, 8))(t[0])
    time_signature.detach()

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    for leaf in t:
        assert contexttools.get_effective_time_signature(leaf) is None
