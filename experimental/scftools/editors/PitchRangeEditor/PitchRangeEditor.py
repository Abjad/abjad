from abjad.tools import pitchtools
from scftools import getters
from scftools.editors.InteractiveEditor import InteractiveEditor
from scftools.editors.TargetManifest import TargetManifest


class PitchRangeEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(pitchtools.PitchRange,
        ('one_line_named_chromatic_pitch_repr', 'rp', getters.get_symbolic_pitch_range_string),
        )
