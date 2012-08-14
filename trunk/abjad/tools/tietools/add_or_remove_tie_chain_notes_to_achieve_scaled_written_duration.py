def add_or_remove_tie_chain_notes_to_achieve_scaled_written_duration(tie_chain, multiplier):
    r'''Add or remove `tie_chain` notes to achieve scaled written duration::

        >>> staff = Staff("c'8 [ ]")

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ ]
        }

    ::
    
        >>> tie_chain = tietools.get_tie_chain(staff[0])
        >>> tietools.add_or_remove_tie_chain_notes_to_achieve_scaled_written_duration(
        ...    tie_chain, Fraction(5, 4))
        TieChain((Note("c'8"), Note("c'32")))

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ ~
            c'32 ]
        }

    Return `tie_chain`.

    .. versionchanged:: 2.0
        renamed ``tietools.duration_scale()`` to
        ``tietools.add_or_remove_tie_chain_notes_to_achieve_scaled_written_duration()``.
    '''
    from abjad.tools import tietools

    # find new tie chain written duration
    new_written_duration = multiplier * tie_chain.written_duration

    # adjust tie chain and return tie chain
    return tietools.add_or_remove_tie_chain_notes_to_achieve_written_duration(tie_chain, new_written_duration)
