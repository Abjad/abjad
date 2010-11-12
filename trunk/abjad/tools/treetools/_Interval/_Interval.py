import copy
from abjad.core import _Immutable
from fractions import Fraction


class _Interval(_Immutable):
    '''A low / high pair, carrying some metadata.'''

    __slots__ = ('data', 'high', 'low', )

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], _Interval):
            low, high, data = args[0].low, args[0].high, args[0].data
        elif len(args) == 2:
            low, high, data = args[0], args[1], None
            if 'data' in kwargs:
                data = kwargs['data']
        elif len(args) == 3:
            low, high, data = args[0], args[1], args[2]
        assert isinstance(low, (int, Fraction))
        assert isinstance(high, (int, Fraction))
        assert low <= high
        if data is not None:
            data = copy.copy(data)
        else:
            data = { }
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

    ## PUBLIC METHODS ##

    def scale_by_value(self, value):
        pass

    def scale_to_value(self, value):
        pass

    def shift_by_value(self, value):
        pass

    def shift_to_value(self, value):
        pass

    def split_at_value(self, value):
        pass
