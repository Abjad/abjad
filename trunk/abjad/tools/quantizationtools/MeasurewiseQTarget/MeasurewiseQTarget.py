import copy
from abjad.tools import measuretools
from abjad.tools import sequencetools
from abjad.tools import voicetools
from abjad.tools.quantizationtools.QTarget import QTarget


class MeasurewiseQTarget(QTarget):
    '''A measure-wise quantization target.

    Not composer-safe.

    Used internally by ``Quantizer``.
    '''

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def beats(self):
        return tuple([beat for item in self.items for beat in item.beats])

    @property
    def item_klass(self):
        from abjad.tools import quantizationtools
        return quantizationtools.QTargetMeasure

    ### PRIVATE METHODS ###

    def _notate(self, grace_handler, attack_point_optimizer, attach_tempo_marks):
        voice = voicetools.Voice()

        # generate the first
        q_target_measure = self.items[0]
        measure = measuretools.Measure(q_target_measure.time_signature)
        for beat in q_target_measure.beats:
            measure.extend(beat.q_grid(beat.beatspan))
        if attach_tempo_marks:
            copy.copy(q_target_measure.tempo)(measure)
        voice.append(measure)

        # generate the rest pairwise, comparing tempi
        for q_target_measure_one, q_target_measure_two in \
            sequencetools.iterate_sequence_pairwise_strict(self.items):
            measure = measuretools.Measure(q_target_measure_two.time_signature)
            for beat in q_target_measure_two.beats:
                measure.extend(beat.q_grid(beat.beatspan))
            if (q_target_measure_two.tempo != q_target_measure_one.tempo) and attach_tempo_marks:
                copy.copy(q_target_measure_two.tempo)(measure)
            voice.append(measure)

        # apply tie chains, pitches, grace containers
        self._notate_leaves_pairwise(voice, grace_handler)

        # partition tiechains in each measure
        for measure in voice:
            attack_point_optimizer(measure)

        return voice
