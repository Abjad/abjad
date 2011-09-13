from abjad.tools.pitchtools._Interval import _Interval
from abjad.tools.pitchtools._Melodic import _Melodic


class _MelodicInterval(_Interval):
    '''.. versionadded:: 2.0

    Melodic interval base class.
    '''

    ### OVERLOADS ###

    def __abs__(self):
        from abjad.tools import pitchtools
        return pitchtools._HarmonicInterval._HarmonicInterval(self)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if arg.number == self.number:
                if arg.direction_number == self.direction_number:
                    return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __neg__(self):
        pass

    # PRIVATE ATTRIUBTES #

    @property
    def _direction_symbol(self):
        if self.direction_number == -1:
            return '-'
        elif self.direction_number == 0:
            return ''
        elif self.direction_number == 1:
            return '+'
        else:
            raise ValueError

    ### PUBLIC ATTRIBUTES ###

    @property
    def direction_number(self):
        return self._direction_number

    @property
    def direction_string(self):
        return self._direction_string
