from abjad.tools.pitchtools.CounterpointIntervalClassObject import CounterpointIntervalClassObject
from abjad.tools.pitchtools.HarmonicIntervalClassObject import HarmonicIntervalClassObject


class HarmonicCounterpointIntervalClass(CounterpointIntervalClassObject, HarmonicIntervalClassObject):
    '''.. versionadded:: 2.0

    Abjad model of harmonic counterpoint interval-class::

        >>> pitchtools.HarmonicCounterpointIntervalClass(-9)
        HarmonicCounterpointIntervalClass(2)

    Harmonic counterpoint interval-classes are immutable.
    '''

    def __init__(self, token):
        from abjad.tools import pitchtools
        if isinstance(token, int):
            _number = token
        elif isinstance(token, (
            pitchtools.DiatonicIntervalObject,
            pitchtools.CounterpointIntervalObject)):
            _number = token.number
        if _number == 0:
            raise ValueError('must be nonzero.')
        if abs(_number) == 1:
            _number = 1
        else:
            _number = abs(_number) % 7
            if _number == 0:
                _number = 7
            elif _number == 1:
                _number = 8
        object.__setattr__(self, '_number', _number)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg
