import copy
from abjad.core import _Immutable
from fractions import Fraction


class _BoundedInterval(_Immutable):
    '''A low / high pair, carrying some metadata.'''

    __slots__ = ('data', 'high', 'low', )

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], _BoundedInterval):
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
    def magnitude(self):
        return self.high - self.low

    @property
    def signature(self):
        return (self.low, self.high)

    ## PUBLIC METHODS ##

    def scale_by_value(self, value):
        assert isinstance(value, (int, Fraction))
        assert 0 <= value
        if value != 1:
            new_magnitude = (self.high - self.low) * value
            return self.__class__(_BoundedInterval(self.low, self.low + new_magnitude, self.data))
        else:
            return self

    def scale_to_value(self, value):
        assert isinstance(value, (int, Fraction))
        assert 0 <= value
        if value != self.magnitude:
            return self.__class__(_BoundedInterval(self.low, self.low + value, self.data))
        else:
            return self

    def shift_by_value(self, value):
        assert isinstance(value, (int, Fraction))
        if value != 0:
            return self.__class__(_BoundedInterval(self.low + value, self.high + value, self.data))
        else:
            return self

    def shift_to_value(self, value):
        assert isinstance(value, (int, Fraction))
        if value != self.low:
            magnitude = self.high - self.low
            return self.__class__(_BoundedInterval(value, value + magnitude, self.data))
        else:
            return self

    def split_at_value(self, value):
        assert isinstance(value, (int, Fraction))
        if self.low < value < self.high:
            return (self.__class__(_BoundedInterval(self.low, value, self.data)),
                    self.__class__(_BoundedInterval(value, self.high, self.data)))
        else:
            return self            
