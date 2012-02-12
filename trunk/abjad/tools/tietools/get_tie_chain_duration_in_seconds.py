from abjad.tools.tietools.is_tie_chain import is_tie_chain


def get_tie_chain_duration_in_seconds(tie_chain):
    '''Return sum of seconds duration of all leaves in chain.

    .. todo:: Write tietools.get_tie_chain_duration_in_seconds() tests.

    .. versionchanged:: 2.0
        renamed ``tietools.get_duration_seconds()`` to
        ``tietools.get_tie_chain_duration_in_seconds()``.
    '''

    assert is_tie_chain(tie_chain)

    try:
        return tie_chain[0].tie.spanner.duration_in_seconds
    except MissingSpannerError:
        return tie_chain[0].duration_in_seconds
