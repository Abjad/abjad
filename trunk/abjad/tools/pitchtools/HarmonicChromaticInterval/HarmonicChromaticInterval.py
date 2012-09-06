import numbers
from abjad.tools.pitchtools.ChromaticIntervalObject import ChromaticIntervalObject
from abjad.tools.pitchtools.HarmonicIntervalObject import HarmonicIntervalObject


class HarmonicChromaticInterval(ChromaticIntervalObject, HarmonicIntervalObject):
    '''.. versionadded:: 2.0

    Abjad model of harmonic chromatic interval::

        >>> pitchtools.HarmonicChromaticInterval(-14)
        HarmonicChromaticInterval(14)

    Harmonic chromatic intervals are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, arg):
        ChromaticIntervalObject.__init__(self, arg)
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

    ### PUBLIC PROPERTIES ###

    @property
    def harmonic_chromatic_interval_class(self):
        '''Read-only harmonic chromatic interval-class::

            >>> harmonic_chromatic_interval = pitchtools.HarmonicChromaticInterval(14)
            >>> harmonic_chromatic_interval.harmonic_chromatic_interval_class
            HarmonicChromaticIntervalClass(2)

        Return harmonic chromatic interval-class.
        '''
        from abjad.tools import pitchtools
        return pitchtools.HarmonicChromaticIntervalClass(self)
