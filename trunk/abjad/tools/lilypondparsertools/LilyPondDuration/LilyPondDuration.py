from abjad.tools.abctools import AbjadObject


class LilyPondDuration(AbjadObject):
    '''Model of a duration in LilyPond.

    Not composer-safe.

    Used internally by LilyPondParser.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('duration', 'multiplier')

    ### INITIALIZER ###

    def __init__(self, duration, multiplier=None):
        self.duration = duration
        self.multiplier = multiplier
