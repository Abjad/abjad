# -*- encoding: utf-8 -*-
from abjad.tools.notetools.Note import Note
from abjad.tools.notetools.Harmonic import Harmonic


class NaturalHarmonic(Note, Harmonic):
    r'''Abjad model of natural harmonic.

    Initialize natural harmonic by hand:

    ::

        >>> notetools.NaturalHarmonic("cs'8.")
        NaturalHarmonic(cs', 8.)

    Initialize natural harmonic from note:

    ::

        >>> note = Note("cs'8.")

    ::

        >>> notetools.NaturalHarmonic(note)
        NaturalHarmonic(cs', 8.)

    Natural harmonics are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        Note.__init__(self, *args)
        self.override.note_head.style = 'harmonic'

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s, %s)' % (
            self._class_name, self.written_pitch, self._formatted_duration)
