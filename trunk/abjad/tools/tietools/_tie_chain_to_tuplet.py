from abjad.exceptions import AssignabilityError
from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import spannertools
from abjad.tools.tietools.TieSpanner import TieSpanner
from abjad.tools.tietools.get_preprolated_tie_chain_duration import get_preprolated_tie_chain_duration
from abjad.tools.tietools.get_tie_chain import get_tie_chain


def _tie_chain_to_tuplet(chain, divisions, prolation, dotted):
    '''.. versionadded:: 2.0

    Generalized tie-chain division function.

    .. todo:: move to tuplettools.
    '''
    from abjad.tools import durationtools
    from abjad.tools import notetools
    from abjad.tools.tuplettools.FixedDurationTuplet import FixedDurationTuplet

    # find target duration of fixed-duration tuplet
    tie_chain = get_tie_chain(chain[0])
    target_duration = get_preprolated_tie_chain_duration(tie_chain)

    # find prolated duration of each note in tuplet
    prolated_duration = target_duration / sum(divisions)

    # find written duration of each notes in tuplet
    if prolation == 'diminution':
        if dotted:
            basic_written_duration = \
                durationtools.rational_to_equal_or_greater_assignable_rational(prolated_duration)
        else:
            basic_written_duration = \
                durationtools.rational_to_equal_or_greater_binary_rational(prolated_duration)
    elif prolation == 'augmentation':
        if dotted:
            basic_written_duration = \
                durationtools.rational_to_equal_or_lesser_assignable_rational(prolated_duration)
        else:
            basic_written_duration = \
                durationtools.rational_to_equal_or_lesser_binary_rational(
                prolated_duration)
    else:
        raise ValueError('must be diminution or augmentation.')

    # find written duration of each note in tuplet
    written_durations = [x * basic_written_duration for x in divisions]

    # make tuplet notes
    try:
        notes = [notetools.Note(0, x) for x in written_durations]
    except AssignabilityError:
        denominator = target_duration._denominator
        note_durations = [durationtools.Duration(x, denominator) for x in divisions]
        notes = notetools.make_notes(0, note_durations)

    # make tuplet
    tuplet = FixedDurationTuplet(target_duration, notes)

    # bequeath tie chain position in score structure to tuplet
    componenttools.move_parentage_and_spanners_from_components_to_components(list(chain), [tuplet])

    # untie tuplet
    #tuplet.tie.unspan()
    spannertools.destroy_all_spanners_attached_to_component(tuplet, TieSpanner)

    # return tuplet
    return tuplet
