from abjad import *


def test_containertools_split_container_by_counts_01():
    '''Partition container into parts of lengths equal to counts.
    Read list of counts cyclically.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    t = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    beamtools.BeamSpanner(t[0])
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

    containertools.split_container_by_counts(t[0], [1, 3], cyclic=True, fracture_spanners=False)

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
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t}\n\t{\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t}\n\t{\n\t\ta'8\n\t\tb'8\n\t\tc''8 ] )\n\t}\n}"


def test_containertools_split_container_by_counts_02():
    '''Cyclic by [1] splits all elements in container.'''

    t = Voice([Container("c'8 d'8 e'8 f'8")])
    beamtools.BeamSpanner(t[0])
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

    containertools.split_container_by_counts(t[0], [1], cyclic=True, fracture_spanners=False)

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
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t}\n\t{\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t}\n\t{\n\t\tf'8 ] )\n\t}\n}"


def test_containertools_split_container_by_counts_03():
    '''Partition container into parts of lengths equal to counts.
    Read list of counts cyclically.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.
    '''

    t = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    beamtools.BeamSpanner(t[0])
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

    parts = containertools.split_container_by_counts(t[0], [1, 3], cyclic=True, fracture_spanners=True)

    r'''
    \new Voice {
        {
            c'8 [ ] (
        }
        {
            d'8 [
            e'8
            f'8 ]
        }
        {
            g'8 [ ]
        }
        {
            a'8 [
            b'8
            c''8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 4
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [ ] (\n\t}\n\t{\n\t\td'8 [\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8 [ ]\n\t}\n\t{\n\t\ta'8 [\n\t\tb'8\n\t\tc''8 ] )\n\t}\n}"


def test_containertools_split_container_by_counts_04():
    '''Cyclic by [1] splits all elements in container.'''

    t = Voice([Container("c'8 d'8 e'8 f'8")])
    beamtools.BeamSpanner(t[0])
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

    parts = containertools.split_container_by_counts(t[0], [1], cyclic=True, fracture_spanners=True)

    r'''
    \new Voice {
        {
            c'8 [ ] (
        }
        {
            d'8 [ ]
        }
        {
            e'8 [ ]
        }
        {
            f'8 [ ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 4
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [ ] (\n\t}\n\t{\n\t\td'8 [ ]\n\t}\n\t{\n\t\te'8 [ ]\n\t}\n\t{\n\t\tf'8 [ ] )\n\t}\n}"


def test_containertools_split_container_by_counts_05():
    '''Partition by large part count.
        Input container cedes contents to new instance.
        Expression appears unaltered.'''

    t = Voice([Container("c'8 d'8 e'8 f'8")])
    beamtools.BeamSpanner(t[0])
    spannertools.SlurSpanner(t[0].leaves)
    container = t[0]

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

    parts = containertools.split_container_by_counts(t[0], [100], cyclic=True, fracture_spanners=True)

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

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 1
    assert container is not t[0]
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t\td'8\n\t\te'8\n\t\tf'8 ] )\n\t}\n}"


def test_containertools_split_container_by_counts_06():
    '''Partition by large number of part counts.
    First part counts apply and extra part counts do not apply.
    Result contains no empty parts.
    '''

    t = Voice([Container("c'8 d'8 e'8 f'8")])
    beamtools.BeamSpanner(t[0])
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

    parts = containertools.split_container_by_counts(t[0], [2, 2, 2, 2, 2], cyclic=True, fracture_spanners=True)

    r'''
    \new Voice {
        {
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 2
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_containertools_split_container_by_counts_07():
    '''Partition by large empty part counts list.
    Empty list returns and expression remains unaltered.
    '''

    t = Voice([Container("c'8 d'8 e'8 f'8")])
    beamtools.BeamSpanner(t[0])
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

    parts = containertools.split_container_by_counts(t[0], [], cyclic=True, fracture_spanners=True)

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

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 1
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t\td'8\n\t\te'8\n\t\tf'8 ] )\n\t}\n}"


def test_containertools_split_container_by_counts_08():
    '''Partition container into parts of lengths equal to counts.
        Read list of counts only once; do not cycle.
        Fracture spanners attaching directly to container.
        Leave spanner attaching to container contents untouched.'''

    t = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    beamtools.BeamSpanner(t[0])
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

    parts = containertools.split_container_by_counts(t[0], [1, 3], cyclic=False, fracture_spanners=False)

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
            a'8
            b'8
            c''8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 3
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t}\n\t{\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t\tb'8\n\t\tc''8 ] )\n\t}\n}"


def test_containertools_split_container_by_counts_09():
    '''Partition container into parts of lengths equal to counts.
    Read list of counts only once; do not cycle.
    Fracture spanners attaching directly to container.
    Leave spanner attaching to container contents untouched.'''

    t = Voice([Container("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    beamtools.BeamSpanner(t[0])
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

    parts = containertools.split_container_by_counts(t[0], [1, 3], cyclic=False, fracture_spanners=True)

    r'''
    \new Voice {
        {
            c'8 [ ] (
        }
        {
            d'8 [
            e'8
            f'8 ]
        }
        {
            g'8 [
            a'8
            b'8
            c''8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 3
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [ ] (\n\t}\n\t{\n\t\td'8 [\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8\n\t\tb'8\n\t\tc''8 ] )\n\t}\n}"


def test_containertools_split_container_by_counts_10():
    '''Partition by large part count.
    Input container cedes contents to new instance.
    Expression appears unaltered.'''

    t = Voice([Container("c'8 d'8 e'8 f'8")])
    beamtools.BeamSpanner(t[0])
    spannertools.SlurSpanner(t[0].leaves)
    container = t[0]

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

    parts = containertools.split_container_by_counts(t[0], [100], cyclic=False, fracture_spanners=True)

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

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 1
    assert container is not t[0]
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t\td'8\n\t\te'8\n\t\tf'8 ] )\n\t}\n}"


def test_containertools_split_container_by_counts_11():
    '''Partition by large number of part counts.
    First part counts apply and extra part counts do not apply.
    Result contains no empty parts.'''

    t = Voice([Container("c'8 d'8 e'8 f'8")])
    beamtools.BeamSpanner(t[0])
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

    parts = containertools.split_container_by_counts(t[0], [2, 2, 2, 2, 2], cyclic=False, fracture_spanners=True)

    r'''
    \new Voice {
        {
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 2
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_containertools_split_container_by_counts_12():
    '''Partition by empty part counts list.
    Input container returns within one-element result list.'''

    t = Voice([Container("c'8 d'8 e'8 f'8")])
    beamtools.BeamSpanner(t[0])
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

    parts = containertools.split_container_by_counts(t[0], [], cyclic=False, fracture_spanners=True)

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

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 1
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [ (\n\t\td'8\n\t\te'8\n\t\tf'8 ] )\n\t}\n}"
