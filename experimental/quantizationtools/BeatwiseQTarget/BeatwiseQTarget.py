import copy
from abjad.tools import containertools
from abjad.tools import sequencetools   
from abjad.tools import voicetools
from experimental.quantizationtools.QTarget import QTarget


class BeatwiseQTarget(QTarget): 
    '''A beat-wise quantization target.

    Not composer-safe.

    Used internally by ``Quantizer``.

    Return ``BeatwiseQTarget`` instance.
    '''

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def beats(self):
        return tuple(self.items)
    
    @property
    def item_klass(self):
        from experimental import quantizationtools
        return quantizationtools.QTargetBeat

    ### PRIVATE METHODS ###

    def _notate(self, grace_handler, attack_point_optimizer, attach_tempo_marks):
        voice = voicetools.Voice()

        # generate the first
        beat = self.items[0]
        components = beat.q_grid(beat.beatspan)
        if attach_tempo_marks:
            attachment_target = components[0]
            if isinstance(attachment_target, containertools.Container):
                attachment_target = attachment_target.leaves[0]
            copy.copy(beat.tempo)(attachment_target)
        voice.extend(components)

        # generate the rest pairwise, comparing tempi
        for beat_one, beat_two in sequencetools.iterate_sequence_pairwise_strict(self.items):
            components = beat_two.q_grid(beat_two.beatspan)
            if (beat_two.tempo != beat_one.tempo) and attach_tempo_marks:
                attachment_target = components[0]
                if isinstance(attachment_target, containertools.Container):
                    attachment_target = attachment_target.leaves[0]
                copy.copy(beat_two.tempo)(attachment_target)
            voice.extend(components)

        # apply tie chains, pitches, grace containers
        self._notate_leaves_pairwise(voice, grace_handler)

        # partition tie chains in voice
        attack_point_optimizer(voice)

        return voice
