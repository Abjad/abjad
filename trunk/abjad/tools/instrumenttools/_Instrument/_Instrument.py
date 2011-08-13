from abjad.tools import contexttools
from abjad.tools import pitchtools


class _Instrument(contexttools.InstrumentMark):
    '''.. versionadded:: 2.0

    Abjad model of the musical instrument.
    '''

    def __init__(self, instrument_name, short_instrument_name, target_context):
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch("c'")
        contexttools.InstrumentMark.__init__(
            self, instrument_name, short_instrument_name, target_context)

    ### PRIVATE METHODS ###

    def _copy_primary_clefs_to_all_clefs(self):
        self.all_clefs = [contexttools.ClefMark(clef) for clef in self.primary_clefs]

    ### PUBLIC ATTRIBUTES ###

    @apply
    def all_clefs( ):
        def fset(self, clefs):
            r'''Read / write all clefs.

            Return tuple of clefs.
            '''
            clefs = [contexttools.ClefMark(clef) for clef in clefs]
            self._all_clefs = clefs
        def fget(self):
            return self._all_clefs
        return property(**locals( ))

    @property
    def interval_of_transposition(self):
        r'''Read-only interval of transposition.

        Return melodic diatonic interval.
        '''
        return pitchtools.NamedChromaticPitch("c'") - self.sounding_pitch_of_fingered_middle_c


    @property
    def is_transposing(self):
        r'''True when instrument is transposing. False otherwise.

        Return boolean.
        '''
        return not self.sounding_pitch_of_fingered_middle_c == pitchtools.NamedChromaticPitch("c'")

    @apply
    def primary_clefs( ):
        def fset(self, clefs):
            r'''Read / write primary clefs.

            Return tuple of clefs.
            '''
            clefs = [contexttools.ClefMark(clef) for clef in clefs]
            self._primary_clefs = clefs
        def fget(self):
            return self._primary_clefs
        return property(**locals( ))

    @apply
    def sounding_pitch_of_fingered_middle_c( ):
        def fset(self, pitch):
            r'''Read / write sounding pitch of fingered middle C.

            Return named chromatic pitch.
            '''
            pitch = pitchtools.NamedChromaticPitch(pitch)
            self._sounding_pitch_of_fingered_middle_c = pitch
        def fget(self):
            return self._sounding_pitch_of_fingered_middle_c
        return property(**locals( ))

    @apply
    def traditional_range( ):
        def fset(self, range):
            r'''Read / write traditional range.

            Return pitch range.
            '''
            range = pitchtools.PitchRange(range)
            self._traditional_range = range
        def fget(self):
            return self._traditional_range
        return property(**locals( ))
