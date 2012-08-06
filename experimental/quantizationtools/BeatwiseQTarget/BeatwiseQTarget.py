from abjad.tools import sequencetools   
from abjad.tools import voicetools
from experimental.quantizationtools.QTarget import QTarget
from experimental.quantizationtools.QTargetBeat import QTargetBeat
import copy


class BeatwiseQTarget(QTarget): 

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def beats(self):
        return tuple(self.items)
    
    @property
    def item_klass(self):
        return QTargetBeat

    ### PRIVATE METHODS ###

    def _notate(self, grace_handler, partitioner):
        voice = voicetools.Voice()

        # generate the first
        beat = self.items[0]
        components = beat.q_grid(beat.beatspan)
        copy.copy(beat.tempo)(components[0])
        voice.extend(components)

        # generate the rest pairwise, comparing tempi
        for beat_one, beat_two in sequencetools.iterate_sequence_pairwise_strict(self.items):
            components = beat_two.q_grid(beat_two.beatspan)
            if beat_two.tempo != beat_one.tempo:
                copy.copy(beat_two.tempo)(components[0])
            voice.extend(components)

        # apply tie chains, pitches, grace containers
        self._notate_leaves_pairwise(voice, grace_handler)

        # partition tie chains in voice
        partitioner(voice)

        return voice
