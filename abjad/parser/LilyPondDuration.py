from abjad.system.AbjadObject import AbjadObject


class LilyPondDuration(AbjadObject):
    """
    Model of a duration in LilyPond.

    Not composer-safe.

    Used internally by LilyPondParser.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        'duration',
        'multiplier',
        )

    ### INITIALIZER ###

    def __init__(self, duration=None, multiplier=None):
        self.duration = duration
        self.multiplier = multiplier
