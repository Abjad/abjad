# -*- coding: utf-8 -*-
import copy
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import scoretools
from abjad.tools.quantizationtools.QTarget import QTarget
from abjad.tools.topleveltools import attach


class MeasurewiseQTarget(QTarget):
    r'''A measure-wise quantization target.

    Not composer-safe.

    Used internally by ``Quantizer``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE METHODS ###

    def _notate(
        self,
        attach_tempos=True,
        attack_point_optimizer=None,
        grace_handler=None,
        ):
        voice = scoretools.Voice()

        # generate the first
        q_target_measure = self.items[0]
        measure = scoretools.Measure(q_target_measure.time_signature)
        for beat in q_target_measure.beats:
            measure.extend(beat.q_grid(beat.beatspan))
        if attach_tempos:
            tempo = copy.copy(q_target_measure.tempo)
            attach(tempo, measure)
        voice.append(measure)

        # generate the rest pairwise, comparing tempi
        for q_target_measure_one, q_target_measure_two in \
            sequencetools.iterate_sequence_nwise(self.items):
            measure = scoretools.Measure(q_target_measure_two.time_signature)
            for beat in q_target_measure_two.beats:
                measure.extend(beat.q_grid(beat.beatspan))
            if (q_target_measure_two.tempo != q_target_measure_one.tempo) \
                and attach_tempos:
                tempo = copy.copy(q_target_measure_two.tempo)
                attach(tempo, measure)
            voice.append(measure)

        # apply logical ties, pitches, grace containers
        self._notate_leaves(
            grace_handler=grace_handler,
            voice=voice,
            )

        # partition logical ties in each measure
        for measure in voice:
            attack_point_optimizer(measure)

        return voice

    ### PUBLIC PROPERTIES ###

    @property
    def beats(self):
        r'''Beats of measurewise q-target.

        Returns tuple.
        '''
        return tuple([beat for item in self.items for beat in item.beats])

    @property
    def item_class(self):
        r'''Item class of measurewise q-target.

        Returns q-target measure class.
        '''
        from abjad.tools import quantizationtools
        return quantizationtools.QTargetMeasure
