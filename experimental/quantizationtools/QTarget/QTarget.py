from abc import abstractmethod, abstractproperty
from abjad.tools import abctools
from abjad.tools import chordtools
from abjad.tools import marktools
from abjad.tools import notetools
from abjad.tools import resttools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools import tietools
from experimental.quantizationtools.ConcatenatingGraceHandler import ConcatenatingGraceHandler
from experimental.quantizationtools.DistanceHeuristic import DistanceHeuristic
from experimental.quantizationtools.GraceHandler import GraceHandler
from experimental.quantizationtools.Heuristic import Heuristic
from experimental.quantizationtools.JobHandler import JobHandler
from experimental.quantizationtools.NaivePartitioner import NaivePartitioner
from experimental.quantizationtools.Partitioner import Partitioner
from experimental.quantizationtools.QEventSequence import QEventSequence
from experimental.quantizationtools.SerialJobHandler import SerialJobHandler
import bisect


class QTarget(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_items',)

    ### INITIALIZATION ###

    def __init__(self, items):
        assert len(items)
        assert all([isinstance(x, self.item_klass) for x in items])
        self._items = tuple(sorted(items, key=lambda x: x.offset_in_ms))

    ### SPECIAL METHODS ###

    def __call__(self, q_event_sequence, grace_handler=None, heuristic=None, job_handler=None,
        partitioner=None):

        assert isinstance(q_event_sequence, QEventSequence)

        if grace_handler is None:
            grace_handler = ConcatenatingGraceHandler()
        assert isinstance(grace_handler, GraceHandler)

        if heuristic is None:
            heuristic = DistanceHeuristic()
        assert isinstance(heuristic, Heuristic)

        if job_handler is None:
            job_handler = SerialJobHandler()
        assert isinstance(job_handler, JobHandler)

        if partitioner is None:
            partitioner = NaivePartitioner()
        assert isinstance(partitioner, Partitioner)

        # parcel QEvents out to each beat
        beats = self.beats
        offsets = sorted([beat.offset_in_ms for beat in beats])
        for q_event in q_event_sequence:
            index = bisect.bisect(offsets, q_event.offset) - 1
            beat = beats[index]
            beat.q_events.append(q_event)

        # generate QuantizationJobs and process with the JobHandler
        jobs = [beat(i) for i, beat in enumerate(beats)]
        jobs = [job for job in jobs if job]
        jobs = job_handler(jobs)
        for job in jobs:
            beats[job.job_id]._q_grids = job.q_grids

        #for i, beat in enumerate(beats):
        #    print i, len(beat.q_grids)
        #    for q_event in beat.q_events:
        #        print '\t{}'.format(q_event.offset)

        # select the best QGrid for each beat, according to the Heuristic
        beats = heuristic(beats)

        # shift QEvents attached to each QGrid's "next downbeat"
        # over to the next QGrid's first leaf - the real downbeat
        self._shift_downbeat_q_events_to_next_q_grid()

        # TODO: handle a final QGrid with QEvents attached to its next_downbeat.
        # TODO: remove a final QGrid with no QEvents

        # convert the QGrid representation into notation,
        # handling grace-note behavior with the GraceHandler
        return self._notate(grace_handler, partitioner)

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

    @abstractmethod
    def _notate(self, grace_handler, partitioner):
        raise NotImplemented

    def _notate_leaves_pairwise(self, voice, grace_handler):
        # check first against second, notating first, tying as necessry
        # keep track of the leaf index, as we're muting the structure as we go
        leaves = list(voice.leaves)
        for i in range(len(leaves) - 1):
            leaf_one, leaf_two = leaves[i], leaves[i + 1]
            leaf_one = self._notate_one_leaf(leaf_one, grace_handler)
            leaves[i] = leaf_one
            if not marktools.get_annotations_attached_to_component(leaf_two):
                klass = tietools.TieSpanner
                spanner = tuple(spannertools.get_spanners_attached_to_component(leaf_one, klass))[0]
                leaf_two = self._copy_leaf_type_and_pitches(leaf_one, leaf_two)
                leaves[i + 1] = leaf_two
                spanner.append(leaf_two)
        # notate final leaf, if necessary
        self._notate_one_leaf(leaves[-1], grace_handler)
        
    def _notate_one_leaf(self, leaf, grace_handler):
        leaf_annotations = marktools.get_annotations_attached_to_component(leaf)
        if leaf_annotations:
            pitches, grace_container = grace_handler(leaf_annotations[0].value)
            if not pitches:
                new_leaf = resttools.Rest(leaf)
            elif 1 < len(pitches):
                new_leaf = chordtools.Chord(leaf)
                new_leaf.written_pitches = pitches
            else:
                new_leaf = notetools.Note(leaf)
                new_leaf.written_pitch = pitches[0]
            if grace_container:
                grace_container(new_leaf)
            leaf.parent[leaf.parent.index(leaf)] = new_leaf
            marktools.move_marks(leaf, new_leaf)
            tietools.TieSpanner(new_leaf)
            return new_leaf
        return leaf

    def _shift_downbeat_q_events_to_next_q_grid(self):
        beats = self.beats
        for one, two in sequencetools.iterate_sequence_pairwise_strict(beats):
            one_q_events = one.q_grid.next_downbeat.q_event_proxies
            two_q_events = two.q_grid.leaves[0].q_event_proxies
            while one_q_events:
                two_q_events.append(one_q_events.pop())

