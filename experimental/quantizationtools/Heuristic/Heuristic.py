from abc import abstractmethod
from abjad.tools import abctools
from experimental.quantizationtools.QTargetBeat import QTargetBeat


class Heuristic(abctools.AbjadObject):

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, q_target_beats):
        assert len(q_target_beats)
        assert all([isinstance(x, QTargetBeat) for x in q_target_beats])
        return self._process(q_target_beats)

    ### PRIVATE METHODS ###

    @abstractmethod
    def _process(self, q_target_beats):
        raise NotImplemented
