def tie_chain_to_augmented_tuplet_with_proportions_and_encourage_dots(tie_chain, proportions):
    r'''.. versionadded:: 2.0

    .. note:: Deprecated. Use ``tietools.tie_chain_to_tuplet_with_proportions()`` instead.

    Change `tie_chain` to augmented fixed-duration tuplet 
    with `proportions` and encourage dots.

    Return non-trivial tuplet as augmentation.

    Allow tupletted notes to carry dots where ``proportions[i] == 1``.

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
        >>> tietools.tie_chain_to_augmented_tuplet_with_proportions_and_encourage_dots(
        ...     tie_chain, [1])
        FixedDurationTuplet(3/16, [c'8.])

    ::

        >>> f(staff)
        \new Staff {
            {
                c'8. [
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
        >>> tietools.tie_chain_to_augmented_tuplet_with_proportions_and_encourage_dots(
        ...     tie_chain, [1, 2])
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
        >>> tietools.tie_chain_to_augmented_tuplet_with_proportions_and_encourage_dots(
        ...     tie_chain, [1, 2, 2])
        FixedDurationTuplet(3/16, [c'64., c'32., c'32.])

    ::

        >>> f(staff)
        \new Staff {
            \fraction \times 8/5 {
                c'64. [
                c'32.
                c'32.
            }
            c'16 ]
        }

    Return fixed-duration tuplet.

    .. versionchanged:: 2.0
        renamed ``divide.tie_chain_into_arbitrary_augmentation_dotted()`` to
        ``tietools.tie_chain_to_augmented_tuplet_with_proportions_and_encourage_dots()``.
    '''
    from abjad.tools.tietools.tie_chain_to_tuplet_with_proportions import tie_chain_to_tuplet_with_proportions

    return tie_chain_to_tuplet_with_proportions(tie_chain, proportions, diminution=False, dotted=True)
