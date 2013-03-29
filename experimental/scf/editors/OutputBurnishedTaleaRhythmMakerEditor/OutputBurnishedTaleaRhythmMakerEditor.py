from abjad.tools import rhythmmakertools
from scf.editors.RhythmMakerEditor import RhythmMakerEditor
from scf.editors.TargetManifest import TargetManifest
from scf import getters


class OutputBurnishedTaleaRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(rhythmmakertools.OutputBurnishedTaleaRhythmMaker,
        ('talea', None, 'ta', getters.get_nonzero_integers, True),
        ('talea_denominator', None, 'de', getters.get_positive_integer_power_of_two, True),
        ('prolation_addenda', None, 'ad', getters.get_integers, False),
        ('lefts', None, 'lf',  getters.get_integers, False),
        ('middles', None, 'mi', getters.get_integers, False),
        ('rights', None, 'rt', getters.get_integers, False),
        ('left_lengths', None, 'll', getters.get_positive_integers, False),
        ('right_lengths', None, 'rl', getters.get_positive_integers, False),
        ('secondary_divisions', None, 'sd', getters.get_integers, False),
        )
