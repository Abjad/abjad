# -*- coding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadObject


class Heuristic(AbjadObject):
    r'''Abstract base class from which concrete ``Heuristic``
    subclases inherit.

    ``Heuristics`` rank ``QGrids`` according to the criteria they
    encapsulate.

    They provide the means by which the quantizer selects a single ``QGrid``
    from all computed ``QGrids`` for any given ``QTargetBeat`` to
    represent that beat.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, q_target_beats):
        r'''Calls heuristic.

        Returns none.
        '''
        from abjad.tools import quantizationtools
        assert len(q_target_beats)
        assert all(isinstance(x, quantizationtools.QTargetBeat)
            for x in q_target_beats)
        return self._process(q_target_beats)

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _process(self, q_target_beats):
        raise NotImplementedError
