from abjad.tools.leaftools._Leaf import _Leaf
import copy
import re


class Chord(_Leaf):
    '''Abjad model of a chord:

    ::

        abjad> Chord([4, 13, 17], (1, 4))
        Chord("<e' cs'' f''>4")

    Return chord instance.
    '''

    __slots__ = ('_note_heads', '_written_pitches', )

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], _Leaf):
            leaf = args[0]
            written_duration = leaf.written_duration
            lilypond_multiplier = leaf.duration_multiplier
            if hasattr(leaf, 'written_pitch'):
                written_pitches = [leaf.written_pitch]
            elif hasattr(leaf, 'written_pitches'):
                written_pitches = leaf.written_pitches
            else:
                written_pitches = []
            self._copy_override_and_set_from_leaf(leaf)
        elif len(args) == 1 and isinstance(args[0], str):
            pattern = '^<(.*)>\s*(.+)'
            match = re.match(pattern, args[0])
            written_pitches, written_duration = match.groups()
            lilypond_multiplier = None
        elif len(args) == 2:
            written_pitches, written_duration = args
            lilypond_multiplier = None
        elif len(args) == 3:
            written_pitches, written_duration, lilypond_multiplier = args
        else:
            raise ValueError('can not initialize chord from "%s".' % str(args))
        _Leaf.__init__(self, written_duration, lilypond_multiplier)
        self.written_pitches = written_pitches
        self._initialize_keyword_values(**kwargs)

    ### OVERLOADS ###

    def __contains__(self, arg):
        from abjad.tools.notetools.NoteHead import NoteHead
        note_head = NoteHead(arg)
        return note_head in self.note_heads

    def __copy__(self, *args):
        new = _Leaf.__copy__(self)
        new.clear()
        for note_head in self.note_heads:
            new_note_head = copy.copy(note_head)
            new.append(new_note_head)
        return new

    __deepcopy__ = __copy__

    def __delitem__(self, i):
        del(self._note_heads[i])

    def __getitem__(self, i):
        return self._note_heads[i]

    def __getnewargs__(self):
        result = []
        result.append(self.written_pitches)
        result.extend(_Leaf.__getnewargs__(self))
        return tuple(result)

    def __len__(self):
        return len(self.note_heads)

    def __setitem__(self, i, arg):
        from abjad.tools.notetools.NoteHead import NoteHead
        if isinstance(arg, NoteHead):
            note_head = arg
        else:
            note_head = NoteHead(arg)
        note_head._client = self
        self._note_heads[i] = note_head
        self._note_heads.sort()

    ### PRIVATE ATTRIBUTES ###

    @property
    def _compact_representation(self):
        return '<%s>%s' % (self._summary, self._formatted_duration)

    @property
    def _summary(self):
        '''Read-only string summary of noteh eads in chord.
        '''
        return ' '.join([str(x) for x in self])

    ### PUBLIC ATTRIBUTES ### 

    @property
    def fingered_pitches(self):
        r"""Read-only fingered pitches::

            abjad> staff = Staff("<c''' e'''>4 <d''' fs'''>4")
            abjad> glockenspiel = instrumenttools.Glockenspiel()(staff)
            abjad> instrumenttools.transpose_notes_and_chords_in_expr_from_sounding_pitch_to_fingered_pitch(staff)

        ::

            abjad> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Glockenspiel }
                \set Staff.shortInstrumentName = \markup { Gkspl. }
                <c' e'>4
                <d' fs'>4
            }

        ::

            abjad> staff[0].fingered_pitches
            (NamedChromaticPitch("c'"), NamedChromaticPitch("e'"))

        Return tuple of named chromatic pitches.
        """
        from abjad.tools import contexttools
        from abjad.tools import pitchtools
        if self.written_pitch_indication_is_at_sounding_pitch:
            instrument = contexttools.get_effective_instrument(self)
            if not instrument:
                raise InstrumentError('effective instrument of note can not be determined.')
            t_n = instrument.interval_of_transposition
            t_n *= -1
            fingered_pitches = [pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, t_n)
                for pitch in self.written_pitches]
            return tuple(fingered_pitches)
        else:
            return self.written_pitches

    @apply
    def note_heads():
        def fget(self):
            '''Get read-only tuple of note heads in chord::

                abjad> chord = Chord([7, 12, 16], (1, 4))
                abjad> chord.note_heads
                (NoteHead("g'"), NoteHead("c''"), NoteHead("e''"))

            Set chord note heads from any iterable::

                abjad> chord = Chord([7, 12, 16], (1, 4))
                abjad> chord.note_heads = [0, 2, 6]
                abjad> chord
                Chord("<c' d' fs'>4")

            '''
            return tuple(self._note_heads)
        def fset(self, note_head_tokens):
            self._note_heads = []
            if isinstance(note_head_tokens, str):
                note_head_tokens = note_head_tokens.split()
            self.extend(note_head_tokens)
        return property(**locals())

    @apply
    def written_pitches():
        def fget(self):
            '''Get read-only tuple of pitches in chord::

                abjad> chord = Chord([7, 12, 16], (1, 4))
                abjad> chord.written_pitches
                (NamedChromaticPitch("g'"), NamedChromaticPitch("c''"), NamedChromaticPitch("e''"))

            Set chord pitches from any iterable::

                abjad> chord = Chord([7, 12, 16], (1, 4))
                abjad> chord.written_pitches = [0, 2, 6]
                abjad> chord
                Chord("<c' d' fs'>4")

            '''
            return tuple([note_head.written_pitch for note_head in self])
        def fset(self, pitch_tokens):
            self.note_heads = pitch_tokens
        return property(**locals())

    @property
    def sounding_pitches(self):
        r"""Read-only sounding pitches::

            abjad> staff = Staff("<c''' e'''>4 <d''' fs'''>4")
            abjad> glockenspiel = instrumenttools.Glockenspiel()(staff)
            abjad> instrumenttools.transpose_notes_and_chords_in_expr_from_sounding_pitch_to_fingered_pitch(staff)

        ::

            abjad> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Glockenspiel }
                \set Staff.shortInstrumentName = \markup { Gkspl. }
                <c' e'>4
                <d' fs'>4
            }

        ::

            abjad> staff[0].sounding_pitches
            (NamedChromaticPitch("c'''"), NamedChromaticPitch("e'''"))

        Return tuple of named chromatic pitches.
        """
        from abjad.tools import contexttools
        from abjad.tools import pitchtools
        if self.written_pitch_indication_is_at_sounding_pitch:
            return self.written_pitches
        else:
            instrument = contexttools.get_effective_instrument(self)
            if not instrument:
                raise InstrumentError('effective instrument of note can not be determined.')
            t_n = instrument.interval_of_transposition
            sounding_pitches = [pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, t_n)
                for pitch in self.written_pitches]
            return tuple(sounding_pitches)

    ### PUBLIC METHODS ### 

    def append(self, note_head_token):
        '''Append `note_head_token` to chord::

            abjad> chord = Chord([4, 13, 17], (1, 4))
            abjad> chord
            Chord("<e' cs'' f''>4")

        ::

            abjad> chord.append(19)
            abjad> chord
            Chord("<e' cs'' f'' g''>4")

        Sort chord note heads automatically after append and return none.
        '''
        from abjad.tools.notetools.NoteHead import NoteHead
        if isinstance(note_head_token, NoteHead):
            note_head = note_head_token
        else:
            note_head = NoteHead(note_head_token)
        note_head._client = self
        self._note_heads.append(note_head)
        self._note_heads.sort()

    def clear(self):
        '''Clear chord::

            abjad> chord = Chord("<e' cs'' f''>4")
            abjad> chord
            Chord("<e' cs'' f''>4")

        ::

            abjad> chord.clear()
            abjad> chord
            Chord('<>4')

        Return none.
        '''
        del(self[:])

    def extend(self, note_head_tokens):
        '''Extend chord with `note_head_tokens`::

            abjad> chord = Chord([4, 13, 17], (1, 4))
            abjad> chord
            Chord("<e' cs'' f''>4")

        ::

            abjad> chord.extend([2, 12, 18])
            abjad> chord
            Chord("<d' e' c'' cs'' f'' fs''>4")

        Sort chord note heads automatically after extend and return none.
        '''
        for note_head_token in note_head_tokens:
            self.append(note_head_token)

    def pop(self, i=-1):
        '''Remove note head at index `i` in chord::

            abjad> chord = Chord([4, 13, 17], (1, 4))
            abjad> chord
            Chord("<e' cs'' f''>4")

        ::

            abjad> chord.pop(1)
            NoteHead("cs''")

        ::

            abjad> chord
            Chord("<e' f''>4")

        Return note head.
        '''
        note_head = self._note_heads.pop(i)
        note_head._client = None
        return note_head

    def remove(self, note_head):
        '''Remove `note_head` from chord::

            abjad> chord = Chord([4, 13, 17], (1, 4))
            abjad> chord
            Chord("<e' cs'' f''>4")

        ::

            abjad> chord.remove(chord[1])
            abjad> chord
            Chord("<e' f''>4")

        Return none.
        '''
        note_head._client = None
        self._note_heads.remove(note_head)
