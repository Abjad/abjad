import copy
import re
from abjad.tools.leaftools.Leaf import Leaf


class Note(Leaf):
    '''.. versionadded:: 1.0

    Abjad model of a note:

    ::

        >>> note = Note("cs''8.")

    ::

        >>> note
        Note("cs''8.")

    ::

        >>> show(note) # doctest: +SKIP

    Return Note instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_note_head', '_pitch', )

    _default_positional_input_arguments = (repr("c'4"), )

    _repr_is_evaluable = True

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from abjad.tools import lilypondparsertools
        from abjad.tools import notetools
        if len(args) == 1 and isinstance(args[0], str):
            string = '{{ {} }}'.format(args[0])
            parsed = lilypondparsertools.LilyPondParser()(string)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            args = [parsed[0]]
        is_cautionary = False
        is_forced = False
        if len(args) == 1 and isinstance(args[0], Leaf):
            leaf = args[0]
            written_duration = leaf.written_duration
            lilypond_multiplier = leaf.duration_multiplier
            if hasattr(leaf, 'written_pitch'):
                pitch = leaf.written_pitch
                is_cautionary = leaf.note_head.is_cautionary
                is_forced = leaf.note_head.is_forced
            elif hasattr(leaf, 'written_pitches') and 0 < len(leaf.written_pitches):
                pitch = leaf.written_pitches[0]
                is_cautionary = leaf.note_heads[0].is_cautionary
                is_forced = leaf.note_heads[0].is_forced
            else:
                pitch = None
            self._copy_override_and_set_from_leaf(leaf)
        elif len(args) == 2:
            pitch, written_duration = args
            lilypond_multiplier = None
        elif len(args) == 3:
            pitch, written_duration, lilypond_multiplier = args
        else:
            raise ValueError('can not initialize note from "%s".' % str(args))
        Leaf.__init__(self, written_duration, lilypond_multiplier)
        if pitch is not None:
            self.note_head = notetools.NoteHead(
                written_pitch=pitch,
                is_cautionary=is_cautionary,
                is_forced=is_forced
                )
        else:
            self.note_head = None
        self._initialize_keyword_values(**kwargs)

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        result = []
        result.append(self.written_pitch)
        result.extend(Leaf.__getnewargs__(self))
        return tuple(result)

    ### PRIVATE PROPERTIES ###

    @property
    def _body(self):
        result = ''
        if self.written_pitch:
            result += str(self.written_pitch)
            if self.note_head.is_forced:
                result += '!'
            if self.note_head.is_cautionary:
                result += '?'
        result += self._formatted_duration
        return [result]

    @property
    def _compact_representation(self):
        return self._body[0]

    @property
    def _compact_representation_with_tie(self):
        from abjad.tools import tietools
        tie_chain = tietools.get_tie_chain(self)
        if 1 < len(tie_chain) and not self is tie_chain[-1]:
            return '{} ~'.format(self._body[0])
        else:
            return self._body[0]

    ### PUBLIC PROPERTIES ###

    @property
    def fingered_pitch(self):
        r'''Read-only fingered pitch of note::

            >>> staff = Staff("d''8 e''8 f''8 g''8")
            >>> piccolo = instrumenttools.Piccolo()(staff)
            >>> instrumenttools.transpose_from_sounding_pitch_to_fingered_pitch(staff)

        ::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Piccolo }
                \set Staff.shortInstrumentName = \markup { Picc. }
                d'8
                e'8
                f'8
                g'8
            }

        ::

            >>> staff[0].fingered_pitch
            NamedChromaticPitch("d'")

        Return named chromatic pitch.
        '''
        from abjad.tools import contexttools
        from abjad.tools import pitchtools
        if self.written_pitch_indication_is_at_sounding_pitch:
            instrument = contexttools.get_effective_instrument(self)
            if not instrument:
                raise InstrumentError('effective instrument of note can not be determined.')
            t_n = instrument.interval_of_transposition
            t_n *= -1
            fingered_pitch = pitchtools.transpose_pitch_carrier_by_melodic_interval(self.written_pitch, t_n)
            return fingered_pitch
        else:
            return self.written_pitch

    @apply
    def note_head():
        def fget(self):
            '''Get note head of note::

                >>> note = Note(13, (3, 16))
                >>> note.note_head
                NoteHead("cs''")

            Set note head of note::

                >>> note = Note(13, (3, 16))
                >>> note.note_head = 14
                >>> note
                Note("d''8.")

            '''
            return self._note_head
        def fset(self, arg):
            from abjad.tools.notetools.NoteHead import NoteHead
            if isinstance(arg, type(None)):
                self._note_head = None
            elif isinstance(arg, NoteHead):
                self._note_head = arg
            else:
                note_head = NoteHead(client=self, written_pitch=arg)
                self._note_head = note_head
        return property(**locals())

    @apply
    def sounding_pitch():
        def fget(self):
            r'''Get sounding pitch of note::

                >>> staff = Staff("d''8 e''8 f''8 g''8")
                >>> piccolo = instrumenttools.Piccolo()(staff)

            ::

                >>> instrumenttools.transpose_from_sounding_pitch_to_fingered_pitch(staff)

            ::

                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { Piccolo }
                    \set Staff.shortInstrumentName = \markup { Picc. }
                    d'8
                    e'8
                    f'8
                    g'8
                }
                >>> staff[0].sounding_pitch
                NamedChromaticPitch("d''")

            Set sounding pitch of note::

                >>> staff[0].sounding_pitch = "dqs''"
                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { Piccolo }
                    \set Staff.shortInstrumentName = \markup { Picc. }
                    dqs'8
                    e'8
                    f'8
                    g'8
                }

            '''
            from abjad.tools import contexttools
            from abjad.tools import pitchtools
            if self.written_pitch_indication_is_at_sounding_pitch:
                return self.written_pitch
            else:
                instrument = contexttools.get_effective_instrument(self)
                if not instrument:
                    raise InstrumentError('effective instrument of note can not be determined.')
                t_n = instrument.interval_of_transposition
                sounding_pitch = pitchtools.transpose_pitch_carrier_by_melodic_interval(self.written_pitch, t_n)
                return sounding_pitch
        def fset(self, arg):
            from abjad.tools import contexttools
            from abjad.tools import pitchtools
            pitch = pitchtools.NamedChromaticPitch(arg)
            if self.written_pitch_indication_is_at_sounding_pitch:
                self.written_pitch = pitch
            else:
                instrument = contexttools.get_effective_instrument(self)
                if not instrument:
                    raise InstrumentError('effective instrument of note can not be determined.')
                t_n = -1 * instrument.interval_of_transposition
                self.written_pitch = pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, t_n)
        return property(**locals())

    @apply
    def written_pitch():
        def fget(self):
            '''Get named pitch of note::

                >>> note = Note(13, (3, 16))
                >>> note.written_pitch
                NamedChromaticPitch("cs''")

            Set named pitch of note::

                >>> note = Note(13, (3, 16))
                >>> note.written_pitch = 14
                >>> note
                Note("d''8.")

            '''
            if self.note_head is not None and hasattr(self.note_head, 'written_pitch'):
                return self._note_head.written_pitch
            else:
                return None
        def fset(self, arg):
            from abjad.tools import pitchtools
            from abjad.tools.notetools.NoteHead import NoteHead
            if arg is None:
                if self.note_head is not None:
                    self.note_head.written_pitch = None
            else:
                if self.note_head is None:
                    self.note_head = NoteHead(self, written_pitch=None)
                else:
                    pitch = pitchtools.NamedChromaticPitch(arg)
                    self.note_head.written_pitch = pitch
        return property(**locals())
