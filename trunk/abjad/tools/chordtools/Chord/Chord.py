import copy
import re
from abjad.tools.leaftools.Leaf import Leaf


class Chord(Leaf):
    '''Abjad model of a chord:

    ::

        >>> chord = Chord([4, 13, 17], (1, 4))

    ::

        >>> chord
        Chord("<e' cs'' f''>4")

    ::

        >>> show(chord) # doctest: +SKIP

    Return Chord instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_note_heads', '_written_pitches', )

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from abjad.tools import lilypondparsertools
        if len(args) == 1 and isinstance(args[0], str):
            input = '{{ {} }}'.format(args[0])
            parsed = lilypondparsertools.LilyPondParser()(input)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            args = [parsed[0]]
        is_cautionary = []
        is_forced = []
        if len(args) == 1 and isinstance(args[0], Leaf):
            leaf = args[0]
            written_duration = leaf.written_duration
            lilypond_multiplier = leaf.duration_multiplier
            if hasattr(leaf, 'written_pitch'):
                written_pitches = [leaf.written_pitch]
                is_cautionary = [leaf.note_head.is_cautionary]
                is_forced = [leaf.note_head.is_forced]
            elif hasattr(leaf, 'written_pitches'):
                written_pitches = leaf.written_pitches
                is_cautionary = [x.is_cautionary for x in leaf.note_heads]
                is_forced = [x.is_forced for x in leaf.note_heads]
            else:
                written_pitches = []
            self._copy_override_and_set_from_leaf(leaf)
        elif len(args) == 2:
            written_pitches, written_duration = args
            lilypond_multiplier = None
        elif len(args) == 3:
            written_pitches, written_duration, lilypond_multiplier = args
        else:
            raise ValueError('can not initialize chord from "%s".' % str(args))
        Leaf.__init__(self, written_duration, lilypond_multiplier)
        self.written_pitches = written_pitches
        for note_head, cautionary, forced in zip(self.note_heads, is_cautionary, is_forced):
            note_head.is_cautionary = cautionary
            note_head.is_forced = forced
        self._initialize_keyword_values(**kwargs)

    ### SPECIAL METHODS ###

    def __contains__(self, arg):
        from abjad.tools.notetools.NoteHead import NoteHead
        note_head = NoteHead(written_pitch=arg)
        return note_head in self.note_heads

    def _copy_with_marks_but_without_children_or_spanners(self):
        new = Leaf._copy_with_marks_but_without_children_or_spanners(self)
        new.clear()
        for note_head in self.note_heads:
            new_note_head = copy.copy(note_head)
            new.append(new_note_head)
        return new

    def __copy__(self, *args):
        return self._copy_with_marks_but_without_children_or_spanners()

    # necessary to ensure deepcopied chords copy note heads correctly
    __deepcopy__ = __copy__

    def __delitem__(self, i):
        del(self._note_heads[i])

    def __getitem__(self, i):
        return self._note_heads[i]

    def __getnewargs__(self):
        result = []
        result.append(self.written_pitches)
        result.extend(Leaf.__getnewargs__(self))
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

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        return '<%s>%s' % (self._summary, self._formatted_duration)

    @property
    def _summary(self):
        '''Read-only string summary of noteh eads in chord.
        '''
        return ' '.join([str(x) for x in self.note_heads])

    ### PUBLIC PROPERTIES ### 

    @property
    def fingered_pitches(self):
        r"""Read-only fingered pitches::

            >>> staff = Staff("<c''' e'''>4 <d''' fs'''>4")
            >>> glockenspiel = instrumenttools.Glockenspiel()(staff)
            >>> instrumenttools.transpose_from_sounding_pitch_to_fingered_pitch(staff)

        ::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Glockenspiel }
                \set Staff.shortInstrumentName = \markup { Gkspl. }
                <c' e'>4
                <d' fs'>4
            }

        ::

            >>> staff[0].fingered_pitches
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

                >>> chord = Chord([7, 12, 16], (1, 4))
                >>> chord.note_heads
                (NoteHead("g'"), NoteHead("c''"), NoteHead("e''"))

            Set chord note heads from any iterable::

                >>> chord = Chord([7, 12, 16], (1, 4))
                >>> chord.note_heads = [0, 2, 6]
                >>> chord
                Chord("<c' d' fs'>4")

            '''
            return tuple(self._note_heads)
        def fset(self, note_heads):
            self._note_heads = []
            if isinstance(note_heads, str):
                note_heads = note_heads.split()
            self.extend(note_heads)
        return property(**locals())

    @property
    def sounding_pitches(self):
        r"""Read-only sounding pitches::

            >>> staff = Staff("<c''' e'''>4 <d''' fs'''>4")
            >>> glockenspiel = instrumenttools.Glockenspiel()(staff)
            >>> instrumenttools.transpose_from_sounding_pitch_to_fingered_pitch(staff)

        ::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Glockenspiel }
                \set Staff.shortInstrumentName = \markup { Gkspl. }
                <c' e'>4
                <d' fs'>4
            }

        ::

            >>> staff[0].sounding_pitches
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

    @apply
    def written_pitches():
        def fget(self):
            '''Get read-only tuple of pitches in chord::

                >>> chord = Chord([7, 12, 16], (1, 4))
                >>> chord.written_pitches
                (NamedChromaticPitch("g'"), NamedChromaticPitch("c''"), NamedChromaticPitch("e''"))

            Set chord pitches from any iterable::

                >>> chord = Chord([7, 12, 16], (1, 4))
                >>> chord.written_pitches = [0, 2, 6]
                >>> chord
                Chord("<c' d' fs'>4")

            '''
            return tuple([note_head.written_pitch for note_head in self])
        def fset(self, pitchs):
            self.note_heads = pitchs
        return property(**locals())

    ### PUBLIC METHODS ### 

    def append(self, note_head):
        '''Append `note_head` to chord::

            >>> chord = Chord([4, 13, 17], (1, 4))
            >>> chord
            Chord("<e' cs'' f''>4")

        ::

            >>> chord.append(19)
            >>> chord
            Chord("<e' cs'' f'' g''>4")

        Sort chord note heads automatically after append and return none.
        '''
        from abjad.tools.notetools.NoteHead import NoteHead
        if isinstance(note_head, NoteHead):
            note_head = note_head
        else:
            note_head = NoteHead(written_pitch=note_head)
        note_head._client = self
        self._note_heads.append(note_head)
        self._note_heads.sort()

    def clear(self):
        '''Clear chord::

            >>> chord = Chord("<e' cs'' f''>4")
            >>> chord
            Chord("<e' cs'' f''>4")

        ::

            >>> chord.clear()
            >>> chord
            Chord('<>4')

        Return none.
        '''
        # these two statements are equivalent;
        # the slice assignment version casues pychecker to blow an exception
        # wherease the explicit call to __delitem__ doesn't.
        #del(self[:])
        self.__delitem__(slice(0, len(self)))

    def extend(self, note_heads):
        '''Extend chord with `note_heads`::

            >>> chord = Chord([4, 13, 17], (1, 4))
            >>> chord
            Chord("<e' cs'' f''>4")

        ::

            >>> chord.extend([2, 12, 18])
            >>> chord
            Chord("<d' e' c'' cs'' f'' fs''>4")

        Sort chord note heads automatically after extend and return none.
        '''
        for note_head in note_heads:
            self.append(note_head)

    def pop(self, i=-1):
        '''Remove note head at index `i` in chord::

            >>> chord = Chord([4, 13, 17], (1, 4))
            >>> chord
            Chord("<e' cs'' f''>4")

        ::

            >>> chord.pop(1)
            NoteHead("cs''")

        ::

            >>> chord
            Chord("<e' f''>4")

        Return note head.
        '''
        note_head = self._note_heads.pop(i)
        note_head._client = None
        return note_head

    def remove(self, note_head):
        '''Remove `note_head` from chord::

            >>> chord = Chord([4, 13, 17], (1, 4))
            >>> chord
            Chord("<e' cs'' f''>4")

        ::

            >>> chord.remove(chord[1])
            >>> chord
            Chord("<e' f''>4")

        Return none.
        '''
        note_head._client = None
        self._note_heads.remove(note_head)
