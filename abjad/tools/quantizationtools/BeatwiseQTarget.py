# -*- coding: utf-8 -*-
import copy
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools.quantizationtools.QTarget import QTarget
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import select


class BeatwiseQTarget(QTarget):
    r'''A beat-wise quantization target.

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
        beat = self.items[0]
        components = beat.q_grid(beat.beatspan)
        if attach_tempos:
            attachment_target = components[0]
            leaves = select(attachment_target).by_leaf()
            if isinstance(attachment_target, scoretools.Container):
                attachment_target = leaves[0]
            tempo = copy.copy(beat.tempo)
            attach(tempo, attachment_target)
        voice.extend(components)

        # generate the rest pairwise, comparing tempi
        for beat_one, beat_two in \
            sequencetools.iterate_sequence_nwise(self.items):
            components = beat_two.q_grid(beat_two.beatspan)
            if (beat_two.tempo != beat_one.tempo) and attach_tempos:
                attachment_target = components[0]
                leaves = select(attachment_target).by_leaf()
                if isinstance(attachment_target, scoretools.Container):
                    attachment_target = leaves[0]
                tempo = copy.copy(beat_two.tempo)
                attach(tempo, attachment_target)
            voice.extend(components)

        # apply logical ties, pitches, grace containers
        self._notate_leaves(
            grace_handler=grace_handler,
            voice=voice,
            )

        # partition logical ties in voice
        attack_point_optimizer(voice)

        return voice

    ### PUBLIC PROPERTIES ###

    @property
    def beats(self):
        r'''Beats of beatwise q-target.
        '''
        return tuple(self.items)

    @property
    def item_class(self):
        r'''Item class of beatwise q-target.
        '''
        from abjad.tools import quantizationtools
        return quantizationtools.QTargetBeat
