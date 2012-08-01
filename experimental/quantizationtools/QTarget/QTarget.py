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

        # parcel QEvents out to each beat
        beats = self.beats
        offsets = sorted([beat.offset for beat in beats])
        for q_event in q_event_sequence:
            index = bisect.bisect(offsets, q_event.offset) - 1
            beat = beats[index]
            beat.q_events.append(q_event)

        # generate QuantizationJobs and process with the JobHandler
        jobs = [beat(i) for i, beat in enumerate(beats)]
        jobs = [job for job in jobs if job]
        jobs = job_handler(jobs)
        for job in jobs:
            beats[job.job_id].q_grids = job.q_grids

        # select the best QGrid for each beat, according to the Heuristic
        heuristic(self)

        # shift QEvents attached to each QGrid's "next downbeat"
        # over to the next QGrid's first leaf - the real downbeat
        self._shift_downbeat_q_events_to_next_q_grid()

        # TODO: handle a final QGrid with QEvents attached to its next_downbeat.
        # TODO: remove a final QGrid with no QEvents

        # convert the QGrid representation into notation,
        # handling grace-note behavior with the GraceHandler
        return self._notate(grace_handler)

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

    def _copy_leaf_type_and_pitches(self, leaf_one, leaf_two):
        index = leaf_two.parent.index(leaf_two)
        duration = leaf_two.written_duration
        if isinstance(leaf_one, notetools.Note):
            new_leaf = notetools.Note(leaf_one.written_pitch, duration)
        elif isinstance(leaf_one, chordtools.Chord):
            new_leaf = chordtools.Chord(leaf_one.written_pitches, duration)
        else:
            new_leaf = resttools.Rest(duration)
        leaf_two.parent[index] = new_leaf
        return new_leaf

    def _notate_leaves_pairwise(self, voice, grace_handler):
        # check first against second, notating first, tying as necessry
        leaves = voice.leaves
        for leaf_one, leaf_two in sequencetools.iterate_sequence_pairwise_strict(leaves):
            leaf_one = self._notate_one_leaf(leaf_one, grace_handler)
            if not marktools.get_annotations_attached_to_component(leaf_two):
                klass = tietools.TieSpanner
                spanner = tuple(spannertools.get_spanners_attached_to_component(leaf_one, klass))
                leaf_two = self._copy_leaf_type_and_pitches(leaf_one, leaf_two)
                if spanner:
                    spanner.append(leaf_two)
                else:
                    klass([leaf_one, leaf_two])
        # notate final leaf, if necessary
        self._notate_one_leaf(leaves[-1], grace_handler)
        
    def _notate_one_leaf(self, leaf, grace_handler):
        leaf_annotations = marktools.get_annotation_attached_to_component(leaf)
        if leaf_annotations:
            pitches, grace_container = grace_handler(leaf_annotations[0])
            if not pitches:
                new_leaf = resttools.Rest(leaf)
            elif len(pitches) == 1:
                new_leaf = chordtools.Chord(leaf)
                new_leaf.written_pitches = pitches
            else:
                new_leaf = notetools.Note(leaf)
                new_leaf.written_pitch = pitches[0]
            if grace_container:
                grace_container(new_leaf)
            leaf.parent[leaf.parent.index(leaf)] = new_leaf
            leaf = new_leaf
        return leaf

    @abstractmethod
    def _notate(self, grace_handler):
        raise NotImplemented

    def _shift_downbeat_q_events_to_next_q_grid(self):
        beats = self.beats
        for one, two in sequencetools.iterate_sequence_pairwise_strict(beats):
            one_q_events = first.q_grid.next_downbeat.q_events
            two_q_events = second.leaves[0].q_events
            while one_q_events:
                two_q_events.append(one_q_events.pop())

