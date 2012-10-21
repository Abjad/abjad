from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools import spannertools
from abjad.tools import tuplettools


def tie_chain_to_tuplet_with_ratio(tie_chain, proportions, is_diminution=True, dotted=True):
    r'''.. versionadded:: 2.0

    Example 1a. Change `tie_chain` to augmented tuplet with proportions ``[1]``.
    Avoid dots::

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
        >>> tietools.tie_chain_to_tuplet_with_ratio(
        ...     tie_chain, [1], is_diminution=False, dotted=False)
        FixedDurationTuplet(3/16, [c'8])

    ::

        >>> f(staff)
        \new Staff {
            \fraction \times 3/2 {
                c'8 [
            }
            c'16 ]
        }

    Exampl 1b. Change `tie_chain` to augment tuplet with proportions ``[1, 2]``.
    Avoid dots::

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
        >>> tietools.tie_chain_to_tuplet_with_ratio(
        ...     tie_chain, [1, 2], is_diminution=False, dotted=False)
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

    Examle 1c. Change `tie_chain` to augmented tuplet with proportions ``[1, 2, 2]``.
    Avoid dots::

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
        >>> tietools.tie_chain_to_tuplet_with_ratio(
        ...     tie_chain, [1, 2, 2], is_diminution=False, dotted=False)
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

    Return tuplet.
    '''
    from abjad.tools import tietools

    # check input
    assert isinstance(tie_chain, tietools.TieChain)
    proportions = mathtools.Ratio(proportions)

    # find target duration of fixed-duration tuplet
    target_duration = tie_chain.preprolated_duration

    # find prolated duration of each note in tuplet
    prolated_duration = target_duration / sum(proportions)

    # find written duration of each notes in tuplet
    if is_diminution:
        if dotted:
            basic_written_duration = \
                durationtools.rational_to_equal_or_greater_assignable_rational(prolated_duration)
        else:
            basic_written_duration = \
                durationtools.rational_to_equal_or_greater_binary_rational(prolated_duration)
    else:
        if dotted:
            basic_written_duration = \
                durationtools.rational_to_equal_or_lesser_assignable_rational(prolated_duration)
        else:
            basic_written_duration = \
                durationtools.rational_to_equal_or_lesser_binary_rational(
                prolated_duration)

    # find written duration of each note in tuplet
    written_durations = [x * basic_written_duration for x in proportions]

    # make tuplet notes
    try:
        notes = [notetools.Note(0, x) for x in written_durations]
    except AssignabilityError:
        denominator = target_duration._denominator
        note_durations = [durationtools.Duration(x, denominator) for x in proportions]
        notes = notetools.make_notes(0, note_durations)

    # make tuplet
    tuplet = tuplettools.FixedDurationTuplet(target_duration, notes)

    # replace tie chain with tuplet
    componenttools.move_parentage_and_spanners_from_components_to_components(list(tie_chain), [tuplet])

    # untie tuplet
    spannertools.destroy_spanners_attached_to_component(tuplet, tietools.TieSpanner)

    # return tuplet
    return tuplet
