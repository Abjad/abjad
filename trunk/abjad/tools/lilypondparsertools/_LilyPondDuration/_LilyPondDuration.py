class _LilyPondDuration(object):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('duration', 'multiplier')

    ### INITIALIZER ###

    def __init__(self, duration, multiplier=None):
        self.duration = duration
        self.multiplier = multiplier
