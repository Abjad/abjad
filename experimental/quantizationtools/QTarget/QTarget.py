from abc import abstractmethod, abstractproperty
from abjad.tools import abctools
from experimental.quantizationtools.DistanceHeuristic import DistanceHeuristic
from experimental.quantizationtools.GraceHandler import GraceHandler
from experimental.quantizationtools.Heuristic import Heuristic
from experimental.quantizationtools.JobHandler import JobHandler
from experimental.quantizationtools.QEventSequence import QEventSequence
from experimental.quantizationtools.SerialJobHandler import SerialJobHandler


class QTarget(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_items',)

    ### INITIALIZATION ###

    def __init__(self, items):
        assert len(items)
        assert all([isinstance(x, self.item_klass) for x in items])
        self._items = tuple(sorted(items, key=lambda x: x.offset_in_ms))

    ### SPECIAL METHODS ###

    def __call__(self, q_event_sequence, grace_handler=None, heuristic=None, job_handler=None):

        assert isinstance(q_event_sequence, QEventSequence)

        if grace_handler is None:
            grace_handler = GraceHandler()
        assert isinstance(grace_handler, GraceHandler)

        if heuristic is None:
            heuristic = DistanceHeuristic()
        assert isinstance(heuristic, Heuristic)

        if job_handler is None:
            job_handler = SingleProcessJobHandler()
        assert isinstance(job_handler, JobHandler)

        beats = self.beats
        offsets = sorted([beat.offset for beat in beats])
        for q_event in q_event_sequence:
            index = bisect.bisect(offsets, q_event.offset) - 1
            beat = beats[index]
            beat.q_events.append(q_event)

        jobs = [beat(i) for i, beat in enumerate(beats)]
        jobs = [job for job in jobs if job]
        jobs = job_handler(jobs)
        for job in jobs:
            beats[job.job_id].q_grids = job.q_grids

        heuristic(self)

        return self.notate(grace_handler)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abstractproperty
    def beats(self):
        raise NotImplemented

    @property
    def duration_in_ms(self):
        last_item = self._items[-1]
        return last_item.offset_in_ms + last_item.duration_in_ms

    @abstractproperty
    def item_klass(self):
        raise NotImplemented

    @property
    def items(self):
        return self._items

    ### PRIVATE METHODS ###

    @abstractmethod
    def _notate(self, grace_handler):
        raise NotImplemented

