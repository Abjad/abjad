from abjad.tools.pitchtools._ChromaticIntervalClass import _ChromaticIntervalClass
from abjad.tools.pitchtools._HarmonicIntervalClass import _HarmonicIntervalClass
import numbers


class HarmonicChromaticIntervalClass(_ChromaticIntervalClass, _HarmonicIntervalClass):
    '''.. versionadded:: 2.0

    Abjad model of harmonic chromatic interval-class::

        abjad> pitchtools.HarmonicChromaticIntervalClass(-14)
        HarmonicChromaticIntervalClass(2)

    Harmonic chromatic interval-classes are immutable.
    '''

    def __new__(klass, token):
        from abjad.tools import pitchtools
        self = object.__new__(klass)
        if isinstance(token, numbers.Number):
            number = token
        elif isinstance(token, pitchtools._Interval._Interval):
            number = token.semitones
        else:
            raise TypeError('must be number or interval instance.')
        if number % 12 == 0 and 12 <= abs(number):
            number = 12
        else:
            number = abs(number) % 12
        object.__setattr__(self, '_number', number)
        return self

    ### OVERLOADS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg
