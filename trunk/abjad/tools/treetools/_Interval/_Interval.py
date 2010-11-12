from abjad.core import _Immutable
from fractions import Fraction


class _Interval(_Immutable):
    '''A low / high pair, carrying some metadata.'''

    __slots__ = ('data', 'high', 'low', )

    def __init__(self, low, high, data = None):
        assert isinstance(low, (int, Fraction))
        assert isinstance(high, (int, Fraction))
        assert low <= high
        object.__setattr__(self, 'low', low)
        object.__setattr__(self, 'high', high)
        object.__setattr__(self, 'data', data)

    ## OVERLOADS ##

    def __repr__(self):
        return '%s(%s, %s, data = %s)' % \
            (self.__class__.__name__, \
             repr(self.low), \
             repr(self.high), \
             repr(self.data))

    ## PUBLIC ATTRIBUTES ##

    @property
    def signature(self):
        return (self.low, self.high)
