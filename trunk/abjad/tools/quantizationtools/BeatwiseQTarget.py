# -*- encoding: utf-8 -*-
import copy
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import scoretools
from abjad.tools.quantizationtools.QTarget import QTarget
from abjad.tools.functiontools import attach


class BeatwiseQTarget(QTarget):
    r'''A beat-wise quantization target.

    Not composer-safe.

    Used internally by ``Quantizer``.

    Return ``BeatwiseQTarget`` instance.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def beats(self):
        return tuple(self.items)

    @property
    def item_class(self):
        from abjad.tools import quantizationtools
        return quantizationtools.QTargetBeat

    ### PRIVATE METHODS ###

    def _notate(self, 
        grace_handler, attack_point_optimizer, attach_tempo_marks):
        voice = scoretools.Voice()

        # generate the first
        beat = self.items[0]
        components = beat.q_grid(beat.beatspan)
        if attach_tempo_marks:
            attachment_target = components[0]
            if isinstance(attachment_target, scoretools.Container):
                attachment_target = attachment_target.select_leaves()[0]
            tempo = copy.copy(beat.tempo)
            attach(tempo, attachment_target)
        voice.extend(components)

        # generate the rest pairwise, comparing tempi
        for beat_one, beat_two in \
            sequencetools.iterate_sequence_pairwise_strict(self.items):
            components = beat_two.q_grid(beat_two.beatspan)
            if (beat_two.tempo != beat_one.tempo) and attach_tempo_marks:
                attachment_target = components[0]
                if isinstance(attachment_target, scoretools.Container):
                    attachment_target = attachment_target.select_leaves()[0]
                tempo = copy.copy(beat_two.tempo)
                attach(tempo, attachment_target)
            voice.extend(components)

        # apply tie chains, pitches, grace containers
        self._notate_leaves_pairwise(voice, grace_handler)

        # partition tie chains in voice
        attack_point_optimizer(voice)

        return voice
