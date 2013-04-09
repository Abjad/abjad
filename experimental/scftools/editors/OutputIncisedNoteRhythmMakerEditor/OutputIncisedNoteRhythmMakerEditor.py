from abjad.tools import rhythmmakertools
from scftools.editors.RhythmMakerEditor import RhythmMakerEditor
from scftools.editors.TargetManifest import TargetManifest
from scftools import getters


class OutputIncisedNoteRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(rhythmmakertools.OutputIncisedNoteRhythmMaker,
        ('prefix_talea', None, 'ps', getters.get_nonzero_integers, True),
        ('prefix_lengths', None, 'pl', getters.get_nonnegative_integers, True),
        ('suffix_talea', None, 'ss', getters.get_nonzero_integers, True),
        ('suffix_lengths', None, 'sl', getters.get_nonnegative_integers, True),
        ('talea_denominator', None, 'de', getters.get_positive_integer_power_of_two, True),
        )
