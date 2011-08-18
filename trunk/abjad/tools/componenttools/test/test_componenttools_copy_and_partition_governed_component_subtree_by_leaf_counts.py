from abjad import *


def test_componenttools_copy_and_partition_governed_component_subtree_by_leaf_counts_01():
    '''Partition tuplet in voice.
        The helper wraps lcopy().
        This means that the original structure remains unchanged.
        Also that resulting parts cut all the way up into voice.'''

    t = Voice([tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")])
    spannertools.BeamSpanner(t[0][:])
    left, right = componenttools.copy_and_partition_governed_component_subtree_by_leaf_counts(t[0], [1, 2])

    r'''
    \new Voice {
        \times 2/3 {
            c'8 [ ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(left)
    assert left.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [ ]\n\t}\n}"

    r'''
    \new Voice {
        \times 2/3 {
            d'8 [
            e'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert right.format == "\\new Voice {\n\t\\times 2/3 {\n\t\td'8 [\n\t\te'8 ]\n\t}\n}"


def test_componenttools_copy_and_partition_governed_component_subtree_by_leaf_counts_02():
    '''Partition voice.'''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    result = componenttools.copy_and_partition_governed_component_subtree_by_leaf_counts(t, [1, 2])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8 ]\n}"

    r'''
    \new Voice {
        c'8 [ ]
    }
    '''

    assert componenttools.is_well_formed_component(result[0])
    assert result[0].format == "\\new Voice {\n\tc'8 [ ]\n}"

    r'''
    \new Voice {
        d'8 [
        e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(result[-1])
    assert result[-1].format == "\\new Voice {\n\td'8 [\n\te'8 ]\n}"
