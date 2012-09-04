def scale_preprolated_leaf_duration(leaf, multiplier):
    r'''.. versionadded:: 1.1

    Scale preprolated `leaf` leaf duration by dotted `multiplier`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beamtools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)
        >>> leaftools.scale_preprolated_leaf_duration(staff[1], Duration(3, 2))
        [Note("d'8.")]
        >>> f(staff)
        \new Staff {
            c'8 [
            d'8.
            e'8
            f'8 ]
        }

    Scale preprolated `leaf` duration by tied `multiplier`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beamtools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)
        >>> leaftools.scale_preprolated_leaf_duration(staff[1], Duration(5, 4))
        [Note("d'8"), Note("d'32")]
        >>> f(staff)
        \new Staff {
            c'8 [
            d'8 ~
            d'32
            e'8
            f'8 ]
        }

    Scale preprolated `leaf` duration by nonbinary `multiplier`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beamtools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)
        >>> leaftools.scale_preprolated_leaf_duration(staff[1], Duration(2, 3))
        [Note("d'8")]
        >>> f(staff)
        \new Staff {
            c'8 [
            \times 2/3 {
                d'8
            }
            e'8
            f'8 ]
        }

    Scale preprolated `leaf` duration by tied nonbinary `multiplier`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beamtools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)
        >>> leaftools.scale_preprolated_leaf_duration(staff[1], Duration(5, 6))
        [Note("d'8"), Note("d'32")]
        >>> f(staff)
        \new Staff {
            c'8 [
            \times 2/3 {
                d'8 ~
                d'32
            }
            e'8
            f'8 ]
        }

    Return `leaf`.

    .. versionchanged:: 2.0
        renamed from ``leaftools.duration_scale()``.
        ``leaftools.scale_preprolated_leaf_duration()``.
    '''
    from abjad.tools import leaftools

    # find new leaf preprolated duration
    new_preprolated_duration = multiplier * leaf.written_duration

    # assign new leaf written duration and return structure
    return leaftools.set_preprolated_leaf_duration(leaf, new_preprolated_duration)
