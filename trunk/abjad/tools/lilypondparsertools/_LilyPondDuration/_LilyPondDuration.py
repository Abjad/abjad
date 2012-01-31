class _LilyPondDuration(object):

    __slots__ = ('duration', 'multiplier')

    def __init__(self, duration, multiplier = None):
        self.duration = duration
        self.multiplier = multiplier
