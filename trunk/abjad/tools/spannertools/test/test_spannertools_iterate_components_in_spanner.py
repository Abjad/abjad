from abjad import *


def test_spannertools_iterate_components_in_spanner_01():

    t = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    p = beamtools.BeamSpanner(t[:])

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [
            d'8
        }
        {
            \time 2/8
            e'8
            f'8 ]
        }
    }
    '''

    components = spannertools.iterate_components_in_spanner(p, reverse=True)
    components = list(components)
    leaves = t.leaves

    assert components[0] is t[-1]
    assert components[1] is leaves[-1]
    assert components[2] is leaves[-2]
    assert components[3] is t[-2]
    assert components[4] is leaves[-3]
    assert components[5] is leaves[-4]


def test_spannertools_iterate_components_in_spanner_02():

    t = Staff("c'8 d'8 e'8 f'8")
    spanner = beamtools.BeamSpanner(t[2:])

    notes = spannertools.iterate_components_in_spanner(spanner, klass=Note)
    assert list(notes) == t[2:]
