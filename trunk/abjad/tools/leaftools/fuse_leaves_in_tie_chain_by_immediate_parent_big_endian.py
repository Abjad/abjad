# TODO: implement corresponding little-endian function
def fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(tie_chain):
    r'''.. versionadded:: 1.1

    Fuse leaves in `tie_chain` by immediate parent::

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
        abjad> leaftools.fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(tie_chain)
        [[Note("c'4")], [Note("c'4")]]

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 2/8
                c'4 ~
            }
            {
                \time 2/8
                c'4
            }
        }

    Return list of fused notes by parent.

    .. versionchanged:: 2.0
        renamed ``fuse.leaves_in_tie_chain()`` to
        ``leaftools.fuse_leaves_in_tie_chain_by_immediate_parent_big_endian()``.
    '''
    from abjad.tools import tietools
    from abjad.tools.leaftools.fuse_leaves_big_endian import fuse_leaves_big_endian

    # check input
    if not tietools.is_tie_chain(tie_chain):
        raise TypeError('must be tie chain.')

    # init result
    result = []

    # group leaves in tie chain by parent
    parts = tietools.group_leaves_in_tie_chain_by_immediate_parents(tie_chain)

    # fuse leaves in each part
    for part in parts:
        result.append(fuse_leaves_big_endian(part))

    # return result
    return result
