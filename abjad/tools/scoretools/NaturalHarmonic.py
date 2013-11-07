# -*- encoding: utf-8 -*-
from abjad.tools.functiontools import override
from abjad.tools.scoretools.Leaf import Leaf


class NaturalHarmonic(Leaf):
    r'''A natural harmonic.

    ..  container:: example

        Initializes from string:


        ::

            >>> harmonic = scoretools.NaturalHarmonic("cs'8.")
            >>> show(harmonic) # doctest: +SKIP

    ..  container:: example

        Initializes from note:

        ::

            >>> note = Note("cs'8.")

        ::

            >>> harmonic = scoretools.NaturalHarmonic(note)
            >>> show(harmonic) # doctest: +SKIP

    Natural harmonics are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_note',
        '_note_head',
        '_pitch',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import scoretools
        note = scoretools.Note(*args)
        override(note).note_head.style = 'harmonic'
        self._note = note
        Leaf.__init__(
            self, 
            self._note.written_duration,
            self._note.lilypond_duration_multiplier,
            )

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats natural harmonic.

        Set `format_specification` to `''` or `'lilypond'`.
        Interprets `''` equal to `'lilypond'`.

        ::

            >>> print format(harmonic)
            \once \override NoteHead #'style = #'harmonic
            cs'8.

        Returns string.
        '''
        return self._note.__format__(format_specification=format_specification)

    def __repr__(self):
        r'''Interpreter representation of natural harmonic.

        Returns string.
        '''
        result = repr(self._note)
        result = result.replace('Note', type(self).__name__)
        return result

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

    ### PUBLIC PROPERTIES ###

    @apply
    def note_head():
        def fget(self):
            r'''Gets and sets note head of natural harmonic.

            Returns note head.
            '''
            return self._note.note_head
        def fset(self, expr):
            self._note.note_head = expr
        return property(**locals())

    @apply
    def written_pitch():
        def fget(self):
            r'''Gets and sets written pitch of natural harmonic.

            Returns named pitch.
            '''
            return self._note.written_pitch
        def fset(self, expr):
            self._note.written_pitch = expr
        return property(**locals())
