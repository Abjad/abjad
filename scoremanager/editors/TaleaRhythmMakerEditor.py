# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from scoremanager import getters
from scoremanager.editors.RhythmMakerEditor import RhythmMakerEditor


class TaleaRhythmMakerEditor(RhythmMakerEditor):
    r'''TaleaRhythmMaker editor.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            rhythmmakertools.TaleaRhythmMaker,
            ('talea', None, 'ta', getters.get_nonzero_integers, True),
            ('talea_denominator', None, 'de', 
                getters.get_positive_integer_power_of_two, True),
            ('extra_counts_per_division', None, 'ad', getters.get_integers, False),
            ('split_divisions_by_counts', None, 'sd', getters.get_integers, False),
            )
