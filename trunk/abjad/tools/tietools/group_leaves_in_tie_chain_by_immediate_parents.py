from abjad.tools.tietools.is_tie_chain import is_tie_chain
import itertools


def group_leaves_in_tie_chain_by_immediate_parents(tie_chain):
    r'''Group leaves in `tie_chain` by immediate parent::

        abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        abjad> tietools.TieSpanner(staff.leaves)
        TieSpanner(c'8, c'8, c'8, c'8)
        abjad> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8 ~
                c'8 ~
            }
            {
                \time 2/8
                c'8 ~
                c'8
            }
        }

    ::

        abjad> tie_chain = tietools.get_tie_chain(staff.leaves[0])
        abjad> tietools.group_leaves_in_tie_chain_by_immediate_parents(tie_chain)
        [[Note("c'8"), Note("c'8")], [Note("c'8"), Note("c'8")]]

    Return list of leaf group lists.

    .. versionchanged:: 2.0
        renamed ``tietools.group_by_parent()`` to
        ``tietools.group_leaves_in_tie_chain_by_immediate_parents()``.
    '''

    # check input
    if not is_tie_chain(tie_chain):
        raise TypeError('must be tie chain.')

    # create partition with itertools
    result = []
    pairs_generator = itertools.groupby(tie_chain, lambda x: id(x._parentage.parent))
    for key, values_generator in pairs_generator:
        result.append(list(values_generator))

    # return result
    return result
