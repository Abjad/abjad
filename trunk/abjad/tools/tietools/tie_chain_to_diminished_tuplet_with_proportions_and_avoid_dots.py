from abjad.tools.tietools._tie_chain_to_tuplet import _tie_chain_to_tuplet


def tie_chain_to_diminished_tuplet_with_proportions_and_avoid_dots(tie_chain, proportions):
    r'''.. versionadded:: 2.0

    Change `tie_chain` to diminished fixed-duration tuplet with `proportions` and avoid dots.

    Do not allow tupletted notes to carry dots where ``proportions[i] == 1``.

    With proportions ``[1]``::

        abjad> staff = Staff("c'8 [ ~ c'16 c'16 ]")

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [ ~
            c'16
            c'16 ]
        }

    ::

        abjad> tie_chain = tietools.get_tie_chain(staff[0])
        abjad> tietools.tie_chain_to_diminished_tuplet_with_proportions_and_avoid_dots(tie_chain, [1])
        FixedDurationTuplet(3/16, [c'4])

    ::

        abjad> f(staff)
        \new Staff {
            \fraction \times 3/4 {
                c'4 [
            }
            c'16 ]
        }

    With proportions ``[1, 2]``::

        abjad> staff = Staff("c'8 [ ~ c'16 c'16 ]")

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [ ~
            c'16
            c'16 ]
        }

    ::

        abjad> tie_chain = tietools.get_tie_chain(staff[0])
        abjad> tietools.tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots(tie_chain, [1, 2])
        FixedDurationTuplet(3/16, [c'16, c'8])

    ::

        abjad> f(staff)
        \new Staff {
            {
                c'16 [
                c'8
            }
            c'16 ]
        }

    With proportions ``[1, 2, 2]``::

        abjad> staff = Staff("c'8 [ ~ c'16 c'16 ]")

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [ ~
            c'16
            c'16 ]
        }

    ::

        abjad> tie_chain = tietools.get_tie_chain(staff[0])
        abjad> tietools.tie_chain_to_diminished_tuplet_with_proportions_and_avoid_dots(tie_chain, [1, 2, 2])
        FixedDurationTuplet(3/16, [c'16, c'8, c'8])

    ::

        abjad> f(staff)
        \new Staff {
            \fraction \times 3/5 {
                c'16 [
                c'8
                c'8
            }
            c'16 ]
        }

    Return fixed-duration tuplet.

    .. versionchanged:: 2.0
        renamed ``divide.tie_chain_into_arbitrary_diminution_undotted()`` to
        ``tietools.tie_chain_to_diminished_tuplet_with_proportions_and_avoid_dots()``.
    '''
    prolation, dotted = 'diminution', False
    return _tie_chain_to_tuplet(tie_chain, proportions, prolation, dotted)
