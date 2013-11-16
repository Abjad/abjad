# -*- encoding: utf-8 -*-
import abc
import bisect
from abjad.tools import scoretools
from abjad.tools import indicatortools
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools.abctools import AbjadObject
from abjad.tools.topleveltools import attach


class QTarget(AbjadObject):
    r'''Abstract base class from which concrete ``QTarget`` subclasses inherit.

    ``QTarget`` is created by a concrete ``QSchema`` instance, and represents
    the mold into which the timepoints contained by a ``QSequence`` instance
    will be poured, as structured by that ``QSchema`` instance.

    Not composer-safe.

    Used internally by the ``Quantizer``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_items',
        )

    ### INITIALIZATION ###

    def __init__(self, items):
        assert len(items)
        assert all(isinstance(x, self.item_class) for x in items)
        self._items = tuple(sorted(items, key=lambda x: x.offset_in_ms))

    ### SPECIAL METHODS ###

    def __call__(self, q_event_sequence,
        grace_handler=None,
        heuristic=None,
        job_handler=None,
        attack_point_optimizer=None,
        attach_tempos=True
        ):

        from abjad.tools import quantizationtools

        assert isinstance(q_event_sequence, quantizationtools.QEventSequence)

        if grace_handler is None:
            grace_handler = quantizationtools.ConcatenatingGraceHandler()
        assert isinstance(grace_handler, quantizationtools.GraceHandler)

        if heuristic is None:
            heuristic = quantizationtools.DistanceHeuristic()
        assert isinstance(heuristic, quantizationtools.Heuristic)

        if job_handler is None:
            job_handler = quantizationtools.SerialJobHandler()
        assert isinstance(job_handler, quantizationtools.JobHandler)

        if attack_point_optimizer is None:
            attack_point_optimizer = \
                quantizationtools.NaiveAttackPointOptimizer()
        assert isinstance(
            attack_point_optimizer, quantizationtools.AttackPointOptimizer)

        # if next-to-last QEvent is silent, pop the TerminalQEvent,
        # in order to prevent rest-tuplets
        q_events = q_event_sequence
        if isinstance(q_event_sequence[-2], quantizationtools.SilentQEvent):
            q_events = q_event_sequence[:-1]

        # parcel QEvents out to each beat
        beats = self.beats
        offsets = sorted([beat.offset_in_ms for beat in beats])
        for q_event in q_events:
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
        return self._notate(
            grace_handler, attack_point_optimizer, attach_tempos)

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def beats(self):
        raise NotImplemented

    @property
    def duration_in_ms(self):
        last_item = self._items[-1]
        return last_item.offset_in_ms + last_item.duration_in_ms

    @abc.abstractproperty
    def item_class(self):
        raise NotImplemented

    @property
    def items(self):
        return self._items

    ### PRIVATE METHODS ###

    def _copy_leaf_type_and_pitches(self, leaf_one, leaf_two):
        index = leaf_two._get_parentage().parent.index(leaf_two)
        duration = leaf_two.written_duration
        if isinstance(leaf_one, scoretools.Note):
            new_leaf = scoretools.Note(leaf_one.written_pitch, duration)
        elif isinstance(leaf_one, scoretools.Chord):
            new_leaf = scoretools.Chord(leaf_one.written_pitches, duration)
        else:
            new_leaf = scoretools.Rest(duration)
        tempos = leaf_two._get_context_marks(indicatortools.Tempo)
        if tempos:
            tempo = tempos[0]
            attach(tempo, new_leaf)
        leaf_two._get_parentage().parent[index] = new_leaf
        return new_leaf

    @abc.abstractmethod
    def _notate(
        self, grace_handler, attack_point_optimizer, attach_tempos):
        raise NotImplemented

    def _notate_leaves_pairwise(self, voice, grace_handler):
        # check first against second, notating first, tying as necessry
        # keep track of the leaf index, as we're mutating the 
        # structure as we go
        leaves = list(voice.select_leaves())
        for i in range(len(leaves) - 1):
            leaf_one, leaf_two = leaves[i], leaves[i + 1]
            leaf_one = self._notate_one_leaf(leaf_one, grace_handler)
            leaves[i] = leaf_one
            if not leaf_two._get_indicators(indicatortools.Annotation):
                spanner_classes = (spannertools.Tie, )
                spanner = tuple(leaf_one._get_spanners(spanner_classes))[0]
                leaf_two = self._copy_leaf_type_and_pitches(leaf_one, leaf_two)
                leaves[i+1] = leaf_two
                spanner.append(leaf_two)
        # notate final leaf, if necessary
        self._notate_one_leaf(leaves[-1], grace_handler)

    def _notate_one_leaf(self, leaf, grace_handler):
        leaf_annotations = leaf._get_indicators(indicatortools.Annotation)
        tempos = leaf._get_context_marks(indicatortools.Tempo)
        if leaf_annotations:
            pitches, grace_container = grace_handler(leaf_annotations[0].value)
            if not pitches:
                new_leaf = scoretools.Rest(leaf)
            elif 1 < len(pitches):
                new_leaf = scoretools.Chord(leaf)
                new_leaf.written_pitches = pitches
            else:
                new_leaf = scoretools.Note(leaf)
                new_leaf.written_pitch = pitches[0]
            if grace_container:
                grace_container(new_leaf)
            leaf._get_parentage().parent[
                leaf._get_parentage().parent.index(leaf)] = new_leaf
            if tempos:
                tempo = tempos[0]
                attach(tempo, new_leaf)
            tie = spannertools.Tie()
            attach(tie, new_leaf)
            return new_leaf
        return leaf

    def _shift_downbeat_q_events_to_next_q_grid(self):
        beats = self.beats
        for one, two in sequencetools.iterate_sequence_pairwise_strict(beats):
            one_q_events = one.q_grid.next_downbeat.q_event_proxies
            two_q_events = two.q_grid.leaves[0].q_event_proxies
            while one_q_events:
                two_q_events.append(one_q_events.pop())
