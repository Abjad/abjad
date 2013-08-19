# -*- encoding: utf-8 -*-
import numbers
from abjad.tools.pitchtools.NumberedInterval import NumberedInterval


class HarmonicChromaticInterval(NumberedInterval):
    '''Abjad model of harmonic chromatic interval:

    ::

        >>> pitchtools.HarmonicChromaticInterval(-14)
        HarmonicChromaticInterval(14)

    Harmonic chromatic intervals are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, arg):
        NumberedInterval.__init__(self, arg)
        object.__setattr__(self, '_number', abs(self._number))

    ### SPECIAL METHODS ###

    def __ge__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('%s must be harmonic chromatic interval.' % arg)
        return self.number >= arg.number

    def __gt__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('%s must be harmonic chromatic interval.' % arg)
        return self.number > arg.number

    def __le__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('%s must be harmonic chromatic interval.' % arg)
        return self.number <= arg.number

    def __lt__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('%s must be harmonic chromatic interval.' % arg)
        return self.number < arg.number

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate harmonic chromatic interval from `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.HarmonicChromaticInterval.from_pitch_carriers(
            ...     pitchtools.NamedPitch(-2), 
            ...     pitchtools.NamedPitch(12),
            ...     )
            HarmonicChromaticInterval(14)

        Return harmonic chromatic interval.
        '''
        from abjad.tools import pitchtools
        # get melodic chromatic interval
        mci = pitchtools.MelodicChromaticInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2)
        # return harmonic chromatic interval
        return mci.harmonic_chromatic_interval

    ### PUBLIC PROPERTIES ###

    @property
    def harmonic_chromatic_interval_class(self):
        r'''Harmonic chromatic interval-class:

        ::

            >>> harmonic_chromatic_interval = \
            ...     pitchtools.HarmonicChromaticInterval(14)
            >>> harmonic_chromatic_interval.harmonic_chromatic_interval_class
            HarmonicChromaticIntervalClass(2)

        Return harmonic chromatic interval-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.HarmonicChromaticIntervalClass(self)

