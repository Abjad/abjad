# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from abjad.tools.topleveltools import new
from experimental.tools.musicexpressiontools.PayloadExpression \
    import PayloadExpression


class RhythmMakerExpression(PayloadExpression):
    r'''Rhythm-maker payload expression.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload=None):
        assert isinstance(payload, rhythmmakertools.RhythmMaker)
        PayloadExpression.__init__(self, payload=payload)