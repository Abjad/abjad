from abjad.tools.tietools.add_or_remove_tie_chain_notes_to_achieve_written_duration import add_or_remove_tie_chain_notes_to_achieve_written_duration
from abjad.tools.tietools.is_tie_chain import is_tie_chain
from abjad.tools import durationtools


def add_or_remove_tie_chain_notes_to_achieve_scaled_written_duration(tie_chain, multiplier):
    '''Scale tie chain by multiplier.
    Wraps tie_chain_duration_change.
    Returns tie chain.

    .. versionchanged:: 2.0
        renamed ``tietools.duration_scale()`` to
        ``tietools.add_or_remove_tie_chain_notes_to_achieve_scaled_written_duration()``.
    '''

    # find new tie chain written duration
    new_written_duration = multiplier * tie_chain.written_duration

    # assign new tie chain written duration and return tie chain
    return add_or_remove_tie_chain_notes_to_achieve_written_duration(tie_chain, new_written_duration)
