# -*- encoding: utf-8 -*-
from abjad.tools.functiontools import override
from abjad.tools.scoretools.Note import Note


class NaturalHarmonic(Note):
    r'''Abjad model of natural harmonic.

    Initialize natural harmonic by hand:

    ::

        >>> scoretools.NaturalHarmonic("cs'8.")
        NaturalHarmonic(cs', 8.)

    Initialize natural harmonic from note:

    ::

        >>> note = Note("cs'8.")

    ::

        >>> scoretools.NaturalHarmonic(note)
        NaturalHarmonic(cs', 8.)

    Natural harmonics are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        Note.__init__(self, *args)
        override(self).note_head.style = 'harmonic'

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s, %s)' % (
            type(self).__name__, 
            self.written_pitch, 
            self._formatted_duration,
            )
