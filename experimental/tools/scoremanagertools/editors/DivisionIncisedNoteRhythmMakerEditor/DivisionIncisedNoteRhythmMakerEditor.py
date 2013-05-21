from abjad.tools import rhythmmakertools
from experimental.tools.scoremanagertools.editors.RhythmMakerEditor import RhythmMakerEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagertools import getters


class DivisionIncisedNoteRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS VARIABLES ###

    target_manifest = TargetManifest(rhythmmakertools.DivisionIncisedNoteRhythmMaker,
        ('prefix_talea', None, 'ps', getters.get_nonzero_integers, True),
        ('prefix_lengths', None, 'pl', getters.get_nonnegative_integers, True),
        ('suffix_talea', None, 'ss', getters.get_nonzero_integers, True),
        ('suffix_lengths', None, 'sl', getters.get_nonnegative_integers, True),
        ('talea_denominator', None, 'de', getters.get_positive_integer_power_of_two, True),
        )
