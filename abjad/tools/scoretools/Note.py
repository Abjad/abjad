import copy
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import inspect
from .Leaf import Leaf


class Note(Leaf):
    r'''Note.

    ..  container:: example

        >>> note = abjad.Note("cs''8.")
        >>> measure = abjad.Measure((3, 16), [note])
        >>> abjad.show(measure) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(measure)
            { % measure
                \time 3/16
                cs''8.
            } % measure

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Leaves'

    __slots__ = (
        '_note_head',
        )

    ### INITIALIZER ###

    def __init__(self, *arguments):
        import abjad
        from abjad.ly import drums
        assert len(arguments) in (0, 1, 2)
        if len(arguments) == 1 and isinstance(arguments[0], str):
            string = '{{ {} }}'.format(arguments[0])
            parsed = abjad.parse(string)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            arguments = [parsed[0]]
        is_cautionary = False
        is_forced = False
        is_parenthesized = False
        if len(arguments) == 1 and isinstance(arguments[0], Leaf):
            leaf = arguments[0]
            written_pitch = None
            written_duration = leaf.written_duration
            if 'written_pitch' in dir(leaf):
                written_pitch = leaf.note_head.written_pitch
                is_cautionary = leaf.note_head.is_cautionary
                is_forced = leaf.note_head.is_forced
                is_parenthesized = leaf.note_head.is_parenthesized
            elif 'written_pitches' in dir(leaf):
                written_pitches = [x.written_pitch for x in leaf.note_heads]
                if written_pitches:
                    written_pitch = written_pitches[0]
                    is_cautionary = leaf.note_heads[0].is_cautionary
                    is_forced = leaf.note_heads[0].is_forced
                    is_parenthesized = leaf.note_heads[0].is_parenthesized
        elif len(arguments) == 2:
            written_pitch, written_duration = arguments
        elif len(arguments) == 0:
            written_pitch = 'C4'
            written_duration = abjad.Duration(1, 4)
        else:
            message = 'can not initialize note from {!r}.'
            raise ValueError(message.format(arguments))
        Leaf.__init__(self, written_duration)
        if written_pitch is not None:
            if written_pitch not in drums:
                self.note_head = abjad.NoteHead(
                    written_pitch=written_pitch,
                    is_cautionary=is_cautionary,
                    is_forced=is_forced,
                    is_parenthesized=is_parenthesized,
                    )
            else:
                self.note_head = abjad.DrumNoteHead(
                    written_pitch=written_pitch,
                    is_cautionary=is_cautionary,
                    is_forced=is_forced,
                    is_parenthesized=is_parenthesized,
                    )
        else:
            self.note_head = None
        if len(arguments) == 1 and isinstance(arguments[0], Leaf):
            self._copy_override_and_set_from_leaf(arguments[0])

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        return (self.written_pitch, self.written_duration)

    ### PRIVATE METHODS ###

    def _divide(self, pitch=None):
        import abjad
        pitch = pitch or abjad.NamedPitch('b', 3)
        pitch = abjad.NamedPitch(pitch)
        treble = copy.copy(self)
        bass = copy.copy(self)
        detach(abjad.Markup, treble)
        detach(abjad.Markup, bass)
        if treble.written_pitch < pitch:
            treble = abjad.Rest(treble)
        if pitch <= bass.written_pitch:
            bass = abjad.Rest(bass)
        up_markup = self._get_markup(direction=abjad.Up)
        up_markup = [copy.copy(markup) for markup in up_markup]
        down_markup = self._get_markup(direction=abjad.Down)
        down_markup = [copy.copy(markup) for markup in down_markup]
        for markup in up_markup:
            markup(treble)
        for markup in down_markup:
            markup(bass)
        return treble, bass

    def _get_body(self):
        result = []
        if self.note_head is not None and self.note_head.is_parenthesized:
            result.append(r'\parenthesize')
        body = ''
        if self.written_pitch:
            body += str(self.written_pitch)
            if self.note_head.is_forced:
                body += '!'
            if self.note_head.is_cautionary:
                body += '?'
        body += self._get_formatted_duration()
        result.append(body)
        result = ['\n'.join(result)]
        return result

    def _get_compact_representation(self):
        return self._get_body()[0]

    def _get_compact_representation_with_tie(self):
        logical_tie = self._get_logical_tie()
        if 1 < len(logical_tie) and self is not logical_tie[-1]:
            return '{} ~'.format(self._get_body()[0])
        else:
            return self._get_body()[0]

    def _get_sounding_pitch(self):
        import abjad
        if 'sounding pitch' in abjad.inspect(self).get_indicators(str):
            return self.written_pitch
        else:
            instrument = self._get_effective(abjad.Instrument)
            if instrument:
                sounding_pitch = instrument.middle_c_sounding_pitch
            else:
                sounding_pitch = abjad.NamedPitch('C4')
            interval = abjad.NamedPitch('C4') - sounding_pitch
            sounding_pitch = interval.transpose(self.written_pitch)
            return sounding_pitch

    ### PUBLIC PROPERTIES ###

    @property
    def note_head(self):
        r'''Gets and sets note-head of note.

        .. container:: example

            Gets note-head:

            >>> note = abjad.Note(13, (3, 16))
            >>> note.note_head
            NoteHead("cs''")

        ..  container:: example

            Sets note-head:

            >>> note = abjad.Note(13, (3, 16))
            >>> note.note_head = 14
            >>> note
            Note("d''8.")

        Returns note-head.
        '''
        return self._note_head

    @note_head.setter
    def note_head(self, argument):
        from abjad.tools.scoretools.NoteHead import NoteHead
        if isinstance(argument, type(None)):
            self._note_head = None
        elif isinstance(argument, NoteHead):
            self._note_head = argument
        else:
            note_head = NoteHead(client=self, written_pitch=argument)
            self._note_head = note_head

    @property
    def written_duration(self):
        r'''Gets and sets written duration of note.

        ..  container:: example

            Gets written duration of note.

            >>> note = abjad.Note("c'4")
            >>> note.written_duration
            Duration(1, 4)

        ..  container:: example

            Sets written duration of note:

            >>> note.written_duration = abjad.Duration(1, 16)
            >>> note.written_duration
            Duration(1, 16)

        Returns duration
        '''
        return Leaf.written_duration.fget(self)

    @written_duration.setter
    def written_duration(self, argument):
        return Leaf.written_duration.fset(self, argument)

    @property
    def written_pitch(self):
        r'''Gets and sets written pitch of note.

        ..  container:: example

            Gets written pitch of note.

            >>> note = abjad.Note(13, (3, 16))
            >>> note.written_pitch
            NamedPitch("cs''")

        ..  container:: example

            Sets written pitch of note:

            >>> note = abjad.Note(13, (3, 16))
            >>> note.written_pitch = 14
            >>> note
            Note("d''8.")

        Returns named pitch.
        '''
        if self.note_head is not None:
            return self.note_head.written_pitch

    @written_pitch.setter
    def written_pitch(self, argument):
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        if argument is None:
            if self.note_head is not None:
                self.note_head.written_pitch = None
        else:
            if self.note_head is None:
                self.note_head = scoretools.NoteHead(self, written_pitch=None)
            else:
                pitch = pitchtools.NamedPitch(argument)
                self.note_head.written_pitch = pitch
