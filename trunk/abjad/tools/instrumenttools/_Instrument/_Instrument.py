from abjad.tools import contexttools
from abjad.tools import pitchtools


class _Instrument(contexttools.InstrumentMark):
    '''.. versionadded:: 2.0

    Abjad model of the musical instrument.
    '''

    def __init__(self, instrument_name=None, short_instrument_name=None, 
        instrument_name_markup=None, short_instrument_name_markup=None, target_context=None):
        self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch("c'")
        contexttools.InstrumentMark.__init__(self, instrument_name, short_instrument_name,
            instrument_name_markup=instrument_name_markup, 
            short_instrument_name_markup=short_instrument_name_markup, 
            target_context=target_context)
        self._default_performer_names = ['instrumentalist']
        self._is_primary_instrument = False
        self._pitch_range = None

    ### PRIVATE METHODS ###

    def _copy_primary_clefs_to_all_clefs(self):
        self.all_clefs = [contexttools.ClefMark(clef) for clef in self.primary_clefs]

    ### PUBLIC ATTRIBUTES ###

    @apply
    def all_clefs():
        def fset(self, clefs):
            r'''Read / write all clefs.

            Return tuple of clefs.
            '''
            clefs = [contexttools.ClefMark(clef) for clef in clefs]
            self._all_clefs = clefs
        def fget(self):
            return self._all_clefs
        return property(**locals())

    @property
    def interval_of_transposition(self):
        r'''Read-only interval of transposition.

        Return melodic diatonic interval.
        '''
        return pitchtools.NamedChromaticPitch("c'") - self.sounding_pitch_of_fingered_middle_c

    @property
    def is_primary_instrument(self):
        return self._is_primary_instrument

    @property
    def is_secondary_instrument(self):
        return not self.is_primary_instrument

    @property
    def is_transposing(self):
        r'''True when instrument is transposing. False otherwise.

        Return boolean.
        '''
        return not self.sounding_pitch_of_fingered_middle_c == pitchtools.NamedChromaticPitch("c'")

    @apply
    def pitch_range():
        def fset(self, pitch_range):
            r'''Read / write pitch range.

            Return pitch range.
            '''
            if pitch_range is not None:
                pitch_range = pitchtools.PitchRange(pitch_range)
            self._pitch_range = pitch_range
        def fget(self):
            if self._pitch_range is None:
                return self.traditional_pitch_range
            return self._pitch_range
        return property(**locals())

    @apply
    def primary_clefs():
        def fset(self, clefs):
            r'''Read / write primary clefs.

            Return tuple of clefs.
            '''
            clefs = [contexttools.ClefMark(clef) for clef in clefs]
            self._primary_clefs = clefs
        def fget(self):
            return self._primary_clefs
        return property(**locals())

    @apply
    def sounding_pitch_of_fingered_middle_c():
        def fset(self, pitch):
            r'''Read / write sounding pitch of fingered middle C.

            Return named chromatic pitch.
            '''
            pitch = pitchtools.NamedChromaticPitch(pitch)
            self._sounding_pitch_of_fingered_middle_c = pitch
        def fget(self):
            return self._sounding_pitch_of_fingered_middle_c
        return property(**locals())

    @property
    def traditional_pitch_range(self):
        r'''Read-only traditional pitch range.

        Return pitch range.
        '''
        return self._traditional_pitch_range

    ### PUBLIC METHODS ###

    def get_default_performer_name(self, locale=None):
        r'''.. versionadded:: 2.5

        Get default player name.

        Available values for `locale` are ``'en-us'`` and ``'en-uk'``.
        '''
        locale = locale or 'en-us'
        if self._default_performer_names is None:
            performer_name = '{} player'.format(self.default_instrument_name)
            return performer_name
#        elif locale == 'en-us':
#            return self._default_performer_names[0]
#        elif locale == 'en-uk':
#            if 1 <= len(self._default_performer_names):
#                return self._default_performer_names[1]
#            else:
#                return self._default_performer_names[0]
#        else:
#            raise ValueError
        else:
            return self._default_performer_names[-1]

    def get_performer_names(self):
        r'''.. versionadded:: 2.5

        Get performer names.
        '''
        if self._default_performer_names is None:
            performer_name = '{} player'.format(self.default_instrument_name)
            return [performer_name]
        else:
            return self._default_performer_names[:]
