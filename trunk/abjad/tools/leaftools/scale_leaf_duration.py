# -*- encoding: utf-8 -*-


def scale_leaf_duration(leaf, multiplier):
    r'''Scale `leaf` duration by `multiplier`.

    ..  container:: example

        **Example 1.** Scale leaf duration by dotted `multiplier`:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spannertools.BeamSpanner(staff.select_leaves())
            BeamSpanner(c'8, d'8, e'8, f'8)
            >>> leaftools.scale_leaf_duration(staff[1], Duration(3, 2))
            [Note("d'8.")]
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'8 [
                d'8.
                e'8
                f'8 ]
            }

    ..  container:: example

        **Example 2.** Scale `leaf` duration by tied `multiplier`:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spannertools.BeamSpanner(staff.select_leaves())
            BeamSpanner(c'8, d'8, e'8, f'8)
            >>> leaftools.scale_leaf_duration(staff[1], Duration(5, 4))
            [Note("d'8"), Note("d'32")]
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'8 [
                d'8 ~
                d'32
                e'8
                f'8 ]
            }

    ..  container:: example

        **Example 3.** Scale `leaf` duration by `multiplier` without 
        power-of-two denominator:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spannertools.BeamSpanner(staff.select_leaves())
            BeamSpanner(c'8, d'8, e'8, f'8)
            >>> leaftools.scale_leaf_duration(staff[1], Duration(2, 3))
            ContiguousSelection(Note("d'8"),)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'8 [
                \times 2/3 {
                    d'8
                }
                e'8
                f'8 ]
            }

    ..  container:: example

        **Example 4.** Scale `leaf` duration by tied `multiplier` without 
        power-of-two denominator:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spannertools.BeamSpanner(staff.select_leaves())
            BeamSpanner(c'8, d'8, e'8, f'8)
            >>> leaftools.scale_leaf_duration(staff[1], Duration(5, 6))
            [Note("d'8"), Note("d'32")]
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

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
    '''
    from abjad.tools import leaftools

    # find new leaf preprolated duration
    new_preprolated_duration = multiplier * leaf.written_duration

    # assign new leaf written duration and return structure
    return leaftools.set_leaf_duration(leaf, new_preprolated_duration)
