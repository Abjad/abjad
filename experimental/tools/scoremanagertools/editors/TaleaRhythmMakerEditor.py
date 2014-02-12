# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from experimental.tools.scoremanagertools.editors.RhythmMakerEditor \
    import RhythmMakerEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest
from experimental.tools.scoremanagertools import getters


class TaleaRhythmMakerEditor(RhythmMakerEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return TargetManifest(
            rhythmmakertools.TaleaRhythmMaker,
            ('talea', None, 'ta', getters.get_nonzero_integers, True),
            ('talea_denominator', None, 'de', 
                getters.get_positive_integer_power_of_two, True),
            ('extra_counts_per_division', None, 'ad', getters.get_integers, False),
            ('split_divisions_by_counts', None, 'sd', getters.get_integers, False),
            )
