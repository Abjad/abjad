from abjad.tools import pitchtools
from experimental.tools.scftools import getters
from experimental.tools.scftools.editors.InteractiveEditor import InteractiveEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest


class OctaveTranspositionMappingComponentEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(pitchtools.OctaveTranspositionMappingComponent,
        ('source_pitch_range', 'pr', getters.get_symbolic_pitch_range_string),
        ('target_octave_start_pitch', 'sp', getters.get_integer),
        )
