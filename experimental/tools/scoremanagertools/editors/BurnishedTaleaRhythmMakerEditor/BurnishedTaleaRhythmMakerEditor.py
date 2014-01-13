# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from experimental.tools.scoremanagertools.editors.RhythmMakerEditor \
    import RhythmMakerEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest
from experimental.tools.scoremanagertools import getters


class BurnishedTaleaRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS VARIABLES ###

    target_manifest = TargetManifest(
        rhythmmakertools.BurnishedTaleaRhythmMaker,
        ('talea', None, 'ta', getters.get_nonzero_integers, True),
        ('talea_denominator', None, 'de', 
            getters.get_positive_integer_power_of_two, True),
        ('prolation_addenda', None, 'ad', getters.get_integers, False),
        ('secondary_divisions', None, 'sd', getters.get_integers, False),
        )
