# -*- encoding: utf-8 -*-
import copy
import re
from abjad.tools.scoretools.Leaf import Leaf
from abjad.tools.topleveltools import detach


class Note(Leaf):
    '''A note.

    ..  container:: example
        
        **Example.**

        ::

            >>> note = Note("cs''8.")
            >>> measure = Measure((3, 16), [note])
            >>> show(measure) # doctest: +SKIP

        ..  doctest::

            >>> f(measure)
            {
                \time 3/16
                cs''8.
            }


    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_note_head', 
        '_pitch',
        )

    _default_positional_input_arguments = (
        repr("c'4"),
        )

    _repr_is_evaluable = True

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import lilypondparsertools
        from abjad.tools import scoretools
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
            lilypond_duration_multiplier = leaf.lilypond_duration_multiplier
            if hasattr(leaf, 'written_pitch'):
                pitch = leaf.written_pitch
                is_cautionary = leaf.note_head.is_cautionary
                is_forced = leaf.note_head.is_forced
            elif hasattr(leaf, 'written_pitches') and \
                0 < len(leaf.written_pitches):
                pitch = leaf.written_pitches[0]
                is_cautionary = leaf.note_heads[0].is_cautionary
                is_forced = leaf.note_heads[0].is_forced
            else:
                pitch = None
            self._copy_override_and_set_from_leaf(leaf)
        elif len(args) == 2:
            pitch, written_duration = args
            lilypond_duration_multiplier = None
        elif len(args) == 3:
            pitch, written_duration, lilypond_duration_multiplier = args
        else:
            message = 'can not initialize note from {!r}.'
            raise ValueError(message.format(args))
        Leaf.__init__(self, written_duration, lilypond_duration_multiplier)
        if pitch is not None:
            self.note_head = scoretools.NoteHead(
                written_pitch=pitch,
                is_cautionary=is_cautionary,
                is_forced=is_forced
                )
        else:
            self.note_head = None

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
        tie_chain = self._get_tie_chain()
        if 1 < len(tie_chain) and not self is tie_chain[-1]:
            return '{} ~'.format(self._body[0])
        else:
            return self._body[0]

    ### PRIVATE METHODS ###

    def _divide(self, pitch=None):
        from abjad.tools import markuptools
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        pitch = pitch or pitchtools.NamedPitch('b', 3)
        pitch = pitchtools.NamedPitch(pitch)
        treble = copy.copy(self)
        bass = copy.copy(self)
        detach(markuptools.Markup, treble)
        detach(markuptools.Markup, bass)
        if treble.written_pitch < pitch:
            treble = scoretools.Rest(treble)
        if pitch <= bass.written_pitch:
            bass = scoretools.Rest(bass)
        up_markup = self._get_markup(direction=Up)
        up_markup = [copy.copy(markup) for markup in up_markup]
        down_markup = self._get_markup(direction=Down)
        down_markup = [copy.copy(markup) for markup in down_markup]
        for markup in up_markup:
            markup(treble)
        for markup in down_markup:
            markup(bass)
        return treble, bass

    ### PUBLIC PROPERTIES ###

    @apply
    def lilypond_duration_multiplier():
        def fget(self):
            r'''Gets and sets LilyPond duration multiplier of note.

            ..  container:: example

                Gets LilyPond duration multiplier:

                ::

                    >>> note = Note("c'4 * 1/2")
                    >>> note.lilypond_duration_multiplier
                    Multiplier(1, 2)

            ..  container:: example

                Sets LilyPond duration multiplier:

                ::

                    >>> note.lilypond_duration_multiplier = Multiplier(2, 3)
                    >>> format(note)
                    "c'4 * 2/3"

            Returns multiplier.
            '''
            return Leaf.lilypond_duration_multiplier.fget(self)
        def fset(self, expr):
            return Leaf.lilypond_duration_multiplier.fset(self, expr)
        return property(**locals())

    @apply
    def note_head():
        def fget(self):
            r'''Gets and sets note head of note.

            .. container:: example

                Gets note head:

                ::

                    >>> note = Note(13, (3, 16))
                    >>> note.note_head
                    NoteHead("cs''")

            ..  container:: example

                Sets note head:

                ::

                    >>> note = Note(13, (3, 16))
                    >>> note.note_head = 14
                    >>> note
                    Note("d''8.")

            Returns note head.
            '''
            return self._note_head
        def fset(self, arg):
            from abjad.tools.scoretools.NoteHead import NoteHead
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
            r'''Gets and sets sounding pitch of note.

            ..  container:: example

                Gets sounding pitch of note:

                ::

                    >>> staff = Staff("d''8 e''8 f''8 g''8")
                    >>> piccolo = instrumenttools.Piccolo()
                    >>> attach(piccolo, staff)
                    Piccolo()(Staff{4})

                ::

                    >>> instrumenttools.transpose_from_sounding_pitch_to_written_pitch(
                    ...     staff)

                ..  doctest::

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
                    NamedPitch("d''")

            ..  container:: example

                Sets sounding pitch of note:

                ::

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

            Returns named pitch.
            '''
            from abjad.tools import instrumenttools
            from abjad.tools import pitchtools
            if self.written_pitch_indication_is_at_sounding_pitch:
                return self.written_pitch
            else:
                instrument = self._get_effective_context_mark(
                    instrumenttools.Instrument)
                if not instrument:
                    message = 'effective instrument of note'
                    message += ' can not be determined.'
                    raise InstrumentError(message)
                sounding_pitch = instrument.sounding_pitch_of_written_middle_c
                t_n = pitchtools.NamedPitch('C4') - sounding_pitch
                sounding_pitch = \
                    pitchtools.transpose_pitch_carrier_by_interval(
                        self.written_pitch, t_n)
                return sounding_pitch
        def fset(self, arg):
            from abjad.tools import instrumenttools
            from abjad.tools import pitchtools
            pitch = pitchtools.NamedPitch(arg)
            if self.written_pitch_indication_is_at_sounding_pitch:
                self.written_pitch = pitch
            else:
                instrument = self._get_effective_context_mark(
                    instrumenttools.Instrument)
                if not instrument:
                    message = 'effective instrument of note'
                    message += ' can not be determined.'
                    raise InstrumentError(message)
                sounding_pitch = instrument.sounding_pitch_of_written_middle_c
                t_n = pitchtools.NamedPitch('C4') - sounding_pitch
                t_n *= -1
                self.written_pitch = \
                    pitchtools.transpose_pitch_carrier_by_interval(
                        pitch, t_n)
        return property(**locals())

    @apply
    def written_duration():
        def fget(self):
            r'''Gets and sets written duration of note.

            ..  container:: example

                Gets written duration of note.

                ::

                    >>> note = Note("c'4")
                    >>> note.written_duration
                    Duration(1, 4)

            ..  container:: example

                Sets written duration of note:

                ::

                    >>> note.written_duration = Duration(1, 16)
                    >>> note.written_duration
                    Duration(1, 16)

            Returns duration
            '''
            return Leaf.written_duration.fget(self)
        def fset(self, expr):
            return Leaf.written_duration.fset(self, expr)
        return property(**locals())

    @apply
    def written_pitch():
        def fget(self):
            r'''Gets and sets written pitch of note.

            ..  container:: example

                Gets written pitch of note.

                ::

                    >>> note = Note(13, (3, 16))
                    >>> note.written_pitch
                    NamedPitch("cs''")

            ..  container:: example

                Sets written pitch of note:

                ::

                    >>> note = Note(13, (3, 16))
                    >>> note.written_pitch = 14
                    >>> note
                    Note("d''8.")

            Returns named pitch.
            '''
            if self.note_head is not None:
                if hasattr(self.note_head, 'written_pitch'):
                    return self._note_head.written_pitch
        def fset(self, arg):
            from abjad.tools import pitchtools
            from abjad.tools.scoretools.NoteHead import NoteHead
            if arg is None:
                if self.note_head is not None:
                    self.note_head.written_pitch = None
            else:
                if self.note_head is None:
                    self.note_head = NoteHead(self, written_pitch=None)
                else:
                    pitch = pitchtools.NamedPitch(arg)
                    self.note_head.written_pitch = pitch
        return property(**locals())

    ### PUBLIC METHODS ###

    # TODO: create ArtificialHarmonic class;
    #       replace this with ArtificialHarmonic(note, named_interval=None)
    def add_artificial_harmonic(self, named_interval=None):
        r'''Adds artifical harmonic to note at `named_interval`.

        ..  container:: example

            **Example.** Adds artificial harmonic to note 
            at the perfect fourth above.

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> beam = spannertools.BeamSpanner()
                >>> attach(beam, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4 [
                    d'4
                    e'4
                    f'4 ]
                }

            ::

                >>> staff[0].add_artificial_harmonic()
                Chord("<c' f'>4")
                >>> show(staff) # doctest: +SKIP
    
            ..  doctest::

                >>> f(staff)
                \new Staff {
                    <
                        c'
                        \tweak #'style #'harmonic
                        f'
                    >4 [
                    d'4
                    e'4
                    f'4 ]
                }

        Sets `named_interval` to a perfect fourth
        above when ``named_interval=None``.

        Creates new chord from `note`.

        Moves parentage and spanners from `note` to chord.

        Returns chord.
        '''
        from abjad.tools import scoretools
        from abjad.tools import pitchtools
        if named_interval is None:
            named_interval = pitchtools.NamedInterval('perfect', 4)
        chord = scoretools.Chord(self)
        chord.note_heads.append(
            chord.note_heads[0].written_pitch.numbered_pitch._pitch_number)
        chord.note_heads[1].written_pitch = \
            pitchtools.transpose_pitch_carrier_by_interval(
                chord.note_heads[1].written_pitch, named_interval)
        chord.note_heads[1].tweak.style = 'harmonic'
        parent = self._parent
        if self._parent:
            index = parent.index(self)
            parent[index] = chord
        return chord
