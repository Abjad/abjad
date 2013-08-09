# -*- encoding: utf-8 -*-
import copy
import re
from abjad.tools.selectiontools import more
from abjad.tools.leaftools.Leaf import Leaf


class Note(Leaf):
    '''A note.

    ..  container:: example
        
        **Example.**

        ::

            >>> note = Note("cs''8.")
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> f(note)
            cs''8.

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
            lilypond_multiplier = leaf.lilypond_duration_multiplier
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
        tie_chain = self._select_tie_chain()
        if 1 < len(tie_chain) and not self is tie_chain[-1]:
            return '{} ~'.format(self._body[0])
        else:
            return self._body[0]

    ### PRIVATE METHODS ###

    def _divide(self, pitch=None):
        from abjad.tools import markuptools
        from abjad.tools import pitchtools
        from abjad.tools import resttools
        pitch = pitch or pitchtools.NamedChromaticPitch('b', 3)
        pitch = pitchtools.NamedChromaticPitch(pitch)
        treble = copy.copy(self)
        bass = copy.copy(self)
        treble.select().detach_marks(mark_classes=markuptools.Markup)
        bass.select().detach_marks(mark_classes=markuptools.Markup)
        if treble.written_pitch < pitch:
            treble = resttools.Rest(treble)
        if pitch <= bass.written_pitch:
            bass = resttools.Rest(bass)
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

    @property
    def written_pitch(self):
        r'''Fingered pitch of note:

        ::

            >>> staff = Staff("d''8 e''8 f''8 g''8")
            >>> piccolo = instrumenttools.Piccolo()(staff)
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

        ::

            >>> staff[0].written_pitch
            NamedChromaticPitch("d'")

        Return named chromatic pitch.
        '''
        from abjad.tools import contexttools
        from abjad.tools import pitchtools
        if self.written_pitch_indication_is_at_sounding_pitch:
            instrument = self._get_effective_context_mark(
                contexttools.InstrumentMark)
            if not instrument:
                message = 'effective instrument of note can not be determined.'
                raise InstrumentError(message)
            t_n = instrument.interval_of_transposition
            t_n *= -1
            written_pitch = \
                pitchtools.transpose_pitch_carrier_by_melodic_interval(
                    self.written_pitch, t_n)
            return written_pitch
        else:
            return self.written_pitch

    @apply
    def note_head():
        def fget(self):
            r'''Get note head of note:

            ::

                >>> note = Note(13, (3, 16))
                >>> note.note_head
                NoteHead("cs''")

            Set note head of note:

            ::

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
            r'''Get sounding pitch of note:

            ::

                >>> staff = Staff("d''8 e''8 f''8 g''8")
                >>> piccolo = instrumenttools.Piccolo()(staff)

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
                NamedChromaticPitch("d''")

            Set sounding pitch of note:

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

            '''
            from abjad.tools import contexttools
            from abjad.tools import pitchtools
            if self.written_pitch_indication_is_at_sounding_pitch:
                return self.written_pitch
            else:
                instrument = self._get_effective_context_mark(
                    contexttools.InstrumentMark)
                if not instrument:
                    message = 'effective instrument of note'
                    message += ' can not be determined.'
                    raise InstrumentError(message)
                t_n = instrument.interval_of_transposition
                sounding_pitch = \
                    pitchtools.transpose_pitch_carrier_by_melodic_interval(
                        self.written_pitch, t_n)
                return sounding_pitch
        def fset(self, arg):
            from abjad.tools import contexttools
            from abjad.tools import pitchtools
            pitch = pitchtools.NamedChromaticPitch(arg)
            if self.written_pitch_indication_is_at_sounding_pitch:
                self.written_pitch = pitch
            else:
                instrument = self._get_effective_context_mark(
                    contexttools.InstrumentMark)
                if not instrument:
                    message = 'effective instrument of note'
                    message += ' can not be determined.'
                    raise InstrumentError(message)
                t_n = -1 * instrument.interval_of_transposition
                self.written_pitch = \
                    pitchtools.transpose_pitch_carrier_by_melodic_interval(
                        pitch, t_n)
        return property(**locals())

    @apply
    def written_pitch():
        def fget(self):
            r'''Get named pitch of note:

            ::

                >>> note = Note(13, (3, 16))
                >>> note.written_pitch
                NamedChromaticPitch("cs''")

            Set named pitch of note:

            ::

                >>> note = Note(13, (3, 16))
                >>> note.written_pitch = 14
                >>> note
                Note("d''8.")

            '''
            if self.note_head is not None and \
                hasattr(self.note_head, 'written_pitch'):
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

    ### PUBLIC METHODS ###

    def add_artificial_harmonic(self, melodic_diatonic_interval=None):
        r'''Adds artifical harmonic to note at `melodic_diatonic_interval`.

        ..  container:: example

            **Example.** Add artificial harmonic to note 
            at the perfect fourth above.

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> spannertools.BeamSpanner(staff[:])
                BeamSpanner(c'4, d'4, e'4, f'4)
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

        Sets `melodic_diatonic_interval` to a perfect fourth
        above when ``melodic_diatonic_interval=None``.

        Creates new chord from `note`.

        Moves parentage and spanners from `note` to chord.

        Returns chord.
        '''
        from abjad.tools import chordtools
        from abjad.tools import componenttools
        from abjad.tools import pitchtools
        if melodic_diatonic_interval is None:
            melodic_diatonic_interval = \
                pitchtools.MelodicDiatonicInterval('perfect', 4)
        chord = chordtools.Chord(self)
        chord.append(
            chord[0].written_pitch.numbered_chromatic_pitch._chromatic_pitch_number)
        chord[1].written_pitch = \
            pitchtools.transpose_pitch_carrier_by_melodic_interval(
            chord[1].written_pitch, melodic_diatonic_interval)
        chord[1].tweak.style = 'harmonic'
        componenttools.move_parentage_and_spanners_from_components_to_components(
            [self], [chord])
        return chord
