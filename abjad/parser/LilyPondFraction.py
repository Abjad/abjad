from abjad.system.AbjadObject import AbjadObject


class LilyPondFraction(AbjadObject):
    """
    Model of a fraction in LilyPond.

    Not composer-safe.

    Used internally by LilyPondParser.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        'numerator',
        'denominator',
        )

    ### INITIALIZER ###

    def __init__(self, numerator=0, denominator=1):
        self.numerator = numerator
        self.denominator = denominator
