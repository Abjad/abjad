from abjad.tools.scoretools.NoteHead import NoteHead


class DrumNoteHead(NoteHead):
    r'''A drum note head.

    ::

        >>> note_head = scoretools.DrumNoteHead('snare')
        >>> note_head
        DrumNoteHead('snare')

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        written_pitch='snare',
        client=None,
        is_cautionary=None,
        is_forced=None,
        is_parenthesized=None,
        tweak_pairs=(),
        ):
        from abjad.ly import drums
        NoteHead.__init__(
            self,
            written_pitch=None,
            client=client,
            is_cautionary=is_cautionary,
            is_forced=is_forced,
            is_parenthesized=is_parenthesized,
            tweak_pairs=tweak_pairs,
            )
        assert str(written_pitch) in drums
        drum_pitch = drums[str(written_pitch)]
        self._written_pitch = drum_pitch