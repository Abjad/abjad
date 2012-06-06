from abjad.tools.tietools._tie_chain_to_tuplet import _tie_chain_to_tuplet


def tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots(tie_chain, proportions):
    r'''.. versionadded:: 2.0

    Change `tie_chain` to augmented fixed-duration tuplet with `proportions` and avoid dots.

    Do not allow tupletted notes to carry dots where ``proportions[i] == 1``.

    With proportions ``[1]``::

        >>> staff = Staff("c'8 [ ~ c'16 c'16 ]")

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ ~
            c'16
            c'16 ]
        }

    ::

        >>> tie_chain = tietools.get_tie_chain(staff[0])
        >>> tietools.tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots(tie_chain, [1])
        FixedDurationTuplet(3/16, [c'8])

    ::

        >>> f(staff)
        \new Staff {
            \fraction \times 3/2 {
                c'8 [
            }
            c'16 ]
        }

    With proportions ``[1, 2]``::

        >>> staff = Staff("c'8 [ ~ c'16 c'16 ]")

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ ~
            c'16
            c'16 ]
        }

    ::

        >>> tie_chain = tietools.get_tie_chain(staff[0])
        >>> tietools.tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots(tie_chain, [1, 2])
        FixedDurationTuplet(3/16, [c'16, c'8])

    ::

        >>> f(staff)
        \new Staff {
            {
                c'16 [
                c'8
            }
            c'16 ]
        }

    With proportions ``[1, 2, 2]``::

        >>> staff = Staff("c'8 [ ~ c'16 c'16 ]")

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ ~
            c'16
            c'16 ]
        }

    ::

        >>> tie_chain = tietools.get_tie_chain(staff[0])
        >>> tietools.tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots(tie_chain, [1, 2, 2])
        FixedDurationTuplet(3/16, [c'32, c'16, c'16])

    ::

        >>> f(staff)
        \new Staff {
            \fraction \times 6/5 {
                c'32 [
                c'16
                c'16
            }
            c'16 ]
        }

    Return fixed-duration tuplet.

    .. versionchanged:: 2.0
        renamed ``divide.tie_chain_into_arbitrary_augmentation_undotted()`` to
        ``tietools.tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots()``.
    '''
    prolation, dotted = 'augmentation', False
    return _tie_chain_to_tuplet(tie_chain, proportions, prolation, dotted)
