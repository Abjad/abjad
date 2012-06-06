from abjad.tools import mathtools
from abjad.tools.pitchtools.CounterpointIntervalClassObject import CounterpointIntervalClassObject
from abjad.tools.pitchtools.MelodicIntervalClassObject import MelodicIntervalClassObject


class MelodicCounterpointIntervalClass(CounterpointIntervalClassObject, MelodicIntervalClassObject):
    '''.. versionadded:: 2.0

    Abjad model of melodic counterpoint interval-class::

        >>> pitchtools.MelodicCounterpointIntervalClass(-9)
        MelodicCounterpointIntervalClass(-2)

    Melodic counterpoint interval-classes are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_number', )

    ### INITIALIZER ###

    def __init__(self, token):
        from abjad.tools import pitchtools
        if isinstance(token, int):
            number = token
        elif isinstance(token, pitchtools.CounterpointIntervalObject):
            number = token.number
        if number == 0:
            raise ValueError('must be nonzero.')
        if abs(number) == 1:
            object.__setattr__(self, '_number', 1)
        else:
            sign = mathtools.sign(number)
            number = abs(number) % 7
            if number == 0:
                number = 7
            elif number == 1:
                number = 8
            number *= sign
            object.__setattr__(self, '_number', number)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg
