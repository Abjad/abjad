from abjad import *


def test_containertools_split_container_cyclically_by_counts_and_do_not_fracture_crossing_spanners_01():
    '''Partition container into parts of lengths equal to counts.
    Read list of counts cyclically.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    t = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    spannertools.BeamSpanner(t[0])
    spannertools.SlurSpanner(t[0].leaves)

    r'''
    \new Voice {
        {
            c'8 [ (
            d'8
            e'8
            f'8
            g'8
            a'8
            b'8
            c''8 ] )
        }
    }
    '''

    #containertools.split_container_cyclically_by_counts_and_do_not_fracture_crossing_spanners(t[:], [1, 3])
    containertools.split_container_cyclically_by_counts_and_do_not_fracture_crossing_spanners(t[0], [1, 3])

    r'''
    \new Voice {
        {
            c'8 [ (
        }
        {
            d'8
            e'8
            f'8
        }
        {
            g'8
        }
        {
            a'8
            b'8
            c''8 ] )
        }
    }
    '''


    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t}\n\t{\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t}\n\t{\n\t\ta'8\n\t\tb'8\n\t\tc''8 ] )\n\t}\n}"


def test_containertools_split_container_cyclically_by_counts_and_do_not_fracture_crossing_spanners_02():
    '''Cyclic by [1] splits all elements in container.'''

    t = Voice([Container("c'8 d'8 e'8 f'8")])
    spannertools.BeamSpanner(t[0])
    spannertools.SlurSpanner(t[0].leaves)

    r'''
    \new Voice {
        {
            c'8 [ (
            d'8
            e'8
            f'8 ] )
        }
    }
    '''

    #containertools.split_container_cyclically_by_counts_and_do_not_fracture_crossing_spanners(t[:], [1])
    containertools.split_container_cyclically_by_counts_and_do_not_fracture_crossing_spanners(t[0], [1])

    r'''
    \new Voice {
        {
            c'8 [ (
        }
        {
            d'8
        }
        {
            e'8
        }
        {
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t}\n\t{\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t}\n\t{\n\t\tf'8 ] )\n\t}\n}"
