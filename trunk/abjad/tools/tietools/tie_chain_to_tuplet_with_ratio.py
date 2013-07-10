from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools import spannertools
from abjad.tools import tuplettools


def tie_chain_to_tuplet_with_ratio(
    tie_chain,
    proportions,
    dotted=False,
    is_diminution=True,
    ):
    r'''.. versionadded:: 2.9

    Example 1. Change `tie_chain` to diminished tuplet
    and avoid dots:

    ::

        >>> staff = Staff(r"c'8 ~ c'16 cqs''4")
        >>> crescendo = spannertools.HairpinSpanner(staff[:], 'p < f')
        >>> staff.override.dynamic_line_spanner.staff_padding = 3
        >>> time_signature = contexttools.TimeSignatureMark((7, 16))
        >>> time_signature.attach(staff)
        TimeSignatureMark((7, 16))(Staff{3})
        
    ::

        >>> f(staff)
        \new Staff \with {
            \override DynamicLineSpanner #'staff-padding = #3
        } {
            \time 7/16
            c'8 \< \p ~
            c'16
            cqs''4 \f
        }

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> tie_chain = tietools.get_tie_chain(staff[0])
        >>> tietools.tie_chain_to_tuplet_with_ratio(
        ...     tie_chain, 
        ...     [2, 1, 1, 1], 
        ...     is_diminution=True,
        ...     )
        FixedDurationTuplet(3/16, [c'8, c'16, c'16, c'16])

    ::

        >>> f(staff)
        \new Staff \with {
            \override DynamicLineSpanner #'staff-padding = #3
        } {
            \time 7/16
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/5 {
                c'8 \< \p
                c'16
                c'16
                c'16
            }
            cqs''4 \f
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Example 2. Change `tie_chain` to augmented tuplet
    and avoid dots:

    ::

        >>> staff = Staff(r"c'8 ~ c'16 cqs''4")
        >>> crescendo = spannertools.HairpinSpanner(staff[:], 'p < f')
        >>> staff.override.dynamic_line_spanner.staff_padding = 3
        >>> time_signature = contexttools.TimeSignatureMark((7, 16))
        >>> time_signature.attach(staff)
        TimeSignatureMark((7, 16))(Staff{3})
        
    ::

        >>> f(staff)
        \new Staff \with {
            \override DynamicLineSpanner #'staff-padding = #3
        } {
            \time 7/16
            c'8 \< \p ~
            c'16
            cqs''4 \f
        }

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> tie_chain = tietools.get_tie_chain(staff[0])
        >>> tietools.tie_chain_to_tuplet_with_ratio(
        ...     tie_chain, 
        ...     [2, 1, 1, 1], 
        ...     is_diminution=False, 
        ...     )
        FixedDurationTuplet(3/16, [c'16, c'32, c'32, c'32])

    ::

        >>> f(staff)
        \new Staff \with {
            \override DynamicLineSpanner #'staff-padding = #3
        } {
            \time 7/16
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 6/5 {
                c'16 \< \p
                c'32
                c'32
                c'32
            }
            cqs''4 \f
        }

    ::

        >>> show(staff) # doctest: +SKIP

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
                prolated_duration.equal_or_greater_assignable
        else:
            basic_written_duration = \
                prolated_duration.equal_or_greater_power_of_two
    else:
        if dotted:
            basic_written_duration = \
                prolated_duration.equal_or_lesser_assignable
        else:
            basic_written_duration = \
                prolated_duration.equal_or_lesser_power_of_two

    # find written duration of each note in tuplet
    written_durations = [x * basic_written_duration for x in proportions]

    # make tuplet notes
    try:
        notes = [notetools.Note(0, x) for x in written_durations]
    except AssignabilityError:
        denominator = target_duration._denominator
        note_durations = [durationtools.Duration(x, denominator) 
            for x in proportions]
        notes = notetools.make_notes(0, note_durations)

    # make tuplet
    tuplet = tuplettools.FixedDurationTuplet(target_duration, notes)

    # replace tie chain with tuplet
    componenttools.move_parentage_and_spanners_from_components_to_components(
        list(tie_chain), [tuplet])

    # untie tuplet
    spannertools.destroy_spanners_attached_to_component(
        tuplet, tietools.TieSpanner)

    # return tuplet
    return tuplet
