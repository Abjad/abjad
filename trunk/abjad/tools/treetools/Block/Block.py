from abjad.tools.treetools._Interval import _Interval


class Block(_Interval):
    '''An abstract block of musical material occupying some amount of time.'''
    
    __slots__ = ('data', 'high', 'low', )

    def __init__(self, start_offset, duration, data = None):
        _Interval.__init__(self, start_offset, start_offset + duration, data = data)

    ## OVERLOADS ##
    
    def __repr__(self):
        return '%s(%s, %s, data = %s)' % \
            (self.__class__.__name__, \
             repr(self.start_offset), \
             repr(self.duration), \
             repr(self.data))

    ## PUBLIC ATTRIBUTES ##

    @property
    def start_offset(self):
        return self.low

    @property
    def stop_offset(self):
        return self.high

    @property
    def duration(self):
        return self.high - self.low

    ## PUBLIC METHODS ##

    def scale_to_duration(self, duration):
        pass

    def shift_to_offset(self, offset):
        pass

    def split_at_offset(self, offset):
        pass
