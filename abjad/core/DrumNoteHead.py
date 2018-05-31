from .NoteHead import NoteHead


class DrumNoteHead(NoteHead):
    """
    Drum note-head.

    ..  container:: example

        >>> note_head = abjad.DrumNoteHead('snare')
        >>> note_head
        DrumNoteHead('snare')

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Note-heads'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        written_pitch='snare',
        client=None,
        is_cautionary=None,
        is_forced=None,
        is_parenthesized=None,
        tweaks=(),
        ):
        from abjad.ly import drums
        NoteHead.__init__(
            self,
            written_pitch=None,
            client=client,
            is_cautionary=is_cautionary,
            is_forced=is_forced,
            is_parenthesized=is_parenthesized,
            tweaks=tweaks,
            )
        assert str(written_pitch) in drums
        drum_pitch = drums[str(written_pitch)]
        self._written_pitch = drum_pitch
