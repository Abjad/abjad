from abjad.tools import mathtools
from abjad.tools.pitchtools._CounterpointIntervalClass import _CounterpointIntervalClass
from abjad.tools.pitchtools._MelodicIntervalClass import _MelodicIntervalClass


class MelodicCounterpointIntervalClass(_CounterpointIntervalClass, _MelodicIntervalClass):
    '''.. versionadded:: 2.0

    Abjad model of melodic counterpoint interval-class::

        abjad> pitchtools.MelodicCounterpointIntervalClass(-9)
        MelodicCounterpointIntervalClass(-2)

    Melodic counterpoint interval-classes are immutable.
    '''

    __slots__ = ('_number', )

    def __new__(klass, token):
        from abjad.tools import pitchtools
        self = object.__new__(klass)
        if isinstance(token, int):
            number = token
        elif isinstance(token, pitchtools._CounterpointInterval._CounterpointInterval):
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
        return self

    ### OVERLOADS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg
