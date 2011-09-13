from abjad.tools.notetools.Note import Note
from abjad.tools.notetools._Flageolet._Flageolet import _Flageolet


class NaturalHarmonic(Note, _Flageolet):
    '''Abjad model of natural harmonic.

    Initialize natural harmonic by hand::

        abjad> notetools.NaturalHarmonic("cs'8.")
        NaturalHarmonic(cs', 8.)

    Initialize natural harmonic from note::

        abjad> note = Note("cs'8.")

    ::

        abjad> notetools.NaturalHarmonic(note)
        NaturalHarmonic(cs', 8.)

    Natural harmonics are immutable.
    '''

    __slots__ = ()

    def __init__(self, *args):
        Note.__init__(self, *args)
        self.override.note_head.style = 'harmonic'

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s, %s)' % (type(self).__name__, self.written_pitch, self._formatted_duration)
