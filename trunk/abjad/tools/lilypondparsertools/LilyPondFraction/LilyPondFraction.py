# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class LilyPondFraction(AbjadObject):
    r'''Model of a fraction in LilyPond.

    Not composer-safe.

    Used internally by LilyPondParser.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        'numerator', 
        'denominator',
        )

    ### INITIALIZER ###

    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
