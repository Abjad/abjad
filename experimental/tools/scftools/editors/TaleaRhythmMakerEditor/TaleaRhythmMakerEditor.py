from abjad.tools import rhythmmakertools
from experimental.tools.scftools.editors.RhythmMakerEditor import RhythmMakerEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest
from experimental.tools.scftools import getters


class TaleaRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(rhythmmakertools.TaleaRhythmMaker,
        ('talea', None, 'ta', getters.get_nonzero_integers, True),
        ('talea_denominator', None, 'de', getters.get_positive_integer_power_of_two, True),
        ('prolation_addenda', None, 'ad', getters.get_integers, False),
        ('secondary_divisions', None, 'sd', getters.get_integers, False),
        )
