# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.Spanner import Spanner


def TempoSpanner(Spanner):
    r'''Tempo spanner.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )