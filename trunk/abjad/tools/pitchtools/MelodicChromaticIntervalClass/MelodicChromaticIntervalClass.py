from abjad.tools import mathtools
from abjad.tools.pitchtools._ChromaticIntervalClass import _ChromaticIntervalClass
from abjad.tools.pitchtools._MelodicIntervalClass import _MelodicIntervalClass
import numbers


class MelodicChromaticIntervalClass(_ChromaticIntervalClass, _MelodicIntervalClass):
    '''.. versionadded:: 2.0

    Abjad model of melodic chromatic interval-class::

        abjad> pitchtools.MelodicChromaticIntervalClass(-14)
        MelodicChromaticIntervalClass(-2)

    Melodic chromatic interval-classes are immutable.
    '''

    def __new__(klass, token):
        from abjad.tools import pitchtools
        self = object.__new__(klass)
        if isinstance(token, numbers.Number):
            sign = mathtools.sign(token)
            abs_token = abs(token)
            if abs_token % 12 == 0 and 12 <= abs_token:
                number = 12
            else:
                number = abs_token % 12
            number *= sign
        elif isinstance(token, pitchtools._Interval._Interval):
            number = token.semitones
            sign = mathtools.sign(number)
            abs_number = abs(number)
            if abs_number % 12 == 0 and 12 <= abs_number:
                number = 12
            else:
                number = abs_number % 12
            number *= sign
        elif isinstance(token, pitchtools._IntervalClass._IntervalClass):
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
        return self

    ### OVERLOADS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg
