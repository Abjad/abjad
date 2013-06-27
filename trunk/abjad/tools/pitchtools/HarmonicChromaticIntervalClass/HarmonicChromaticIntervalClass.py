import numbers
from abjad.tools.pitchtools.ChromaticIntervalClass import ChromaticIntervalClass
from abjad.tools.pitchtools.HarmonicIntervalClass import HarmonicIntervalClass


class HarmonicChromaticIntervalClass(ChromaticIntervalClass, HarmonicIntervalClass):
    '''.. versionadded:: 2.0

    Abjad model of harmonic chromatic interval-class:

    ::

        >>> pitchtools.HarmonicChromaticIntervalClass(-14)
        HarmonicChromaticIntervalClass(2)

    Harmonic chromatic interval-classes are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, token):
        from abjad.tools import pitchtools
        if isinstance(token, numbers.Number):
            number = token
        elif isinstance(token, pitchtools.Interval):
            number = token.semitones
        else:
            raise TypeError('must be number or interval instance.')
        if number % 12 == 0 and 12 <= abs(number):
            number = 12
        else:
            number = abs(number) % 12
        object.__setattr__(self, '_number', number)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg
