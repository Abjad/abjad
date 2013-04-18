from abjad.tools import mathtools
from abjad.tools.pitchtools.ChromaticIntervalClassObject import ChromaticIntervalClassObject
from abjad.tools.pitchtools.MelodicIntervalClass import MelodicIntervalClass
import numbers


class MelodicChromaticIntervalClass(ChromaticIntervalClassObject, MelodicIntervalClass):
    '''.. versionadded:: 2.0

    Abjad model of melodic chromatic interval-class::

        >>> pitchtools.MelodicChromaticIntervalClass(-14)
        MelodicChromaticIntervalClass(-2)

    Melodic chromatic interval-classes are immutable.
    '''

    def __init__(self, token):
        from abjad.tools import pitchtools
        if isinstance(token, numbers.Number):
            sign = mathtools.sign(token)
            abs_token = abs(token)
            if abs_token % 12 == 0 and 12 <= abs_token:
                number = 12
            else:
                number = abs_token % 12
            number *= sign
        elif isinstance(token, pitchtools.Interval):
            number = token.semitones
            sign = mathtools.sign(number)
            abs_number = abs(number)
            if abs_number % 12 == 0 and 12 <= abs_number:
                number = 12
            else:
                number = abs_number % 12
            number *= sign
        elif isinstance(token, pitchtools.IntervalClass):
            number = token.number
            sign = mathtools.sign(number)
            abs_number = abs(number)
            if abs_number % 12 == 0 and 12 <= abs_number:
                number = 12
            else:
                number = abs_number % 12
            number *= sign
        else:
            raise ValueError('must be number, interval or interval-class.')
        object.__setattr__(self, '_number', number)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg
