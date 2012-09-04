class _LilyPondFraction(object):
    '''Model of a fraction in LilyPond.

    Not composer-safe.

    Used internally by LilyPondParser.
    '''

    __slots__ = ('numerator', 'denominator')

    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
