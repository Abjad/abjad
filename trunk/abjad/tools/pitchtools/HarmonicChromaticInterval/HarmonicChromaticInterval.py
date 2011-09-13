from abjad.tools.pitchtools._ChromaticInterval import _ChromaticInterval
from abjad.tools.pitchtools._HarmonicInterval import _HarmonicInterval
import numbers


class HarmonicChromaticInterval(_ChromaticInterval, _HarmonicInterval):
    '''.. versionadded:: 2.0

    Abjad model of harmonic chromatic interval::

        abjad> pitchtools.HarmonicChromaticInterval(-14)
        HarmonicChromaticInterval(14)

    Harmonic chromatic intervals are immutable.
    '''

    def __new__(klass, arg):
        self = _ChromaticInterval.__new__(klass, arg)
        object.__setattr__(self, '_number', abs(self._number))
        return self

    ### OVERLOADS ###

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

    ### PUBLIC ATTRIBUTES ###

    @property
    def harmonic_chromatic_interval_class(self):
        '''Read-only harmonic chromatic interval-class::

            abjad> harmonic_chromatic_interval = pitchtools.HarmonicChromaticInterval(14)
            abjad> harmonic_chromatic_interval.harmonic_chromatic_interval_class
            HarmonicChromaticIntervalClass(2)

        Return harmonic chromatic interval-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.HarmonicChromaticIntervalClass(self)
