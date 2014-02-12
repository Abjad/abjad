# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class OctaveTranspositionMappingComponentEditor(InteractiveEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return TargetManifest(
            pitchtools.OctaveTranspositionMappingComponent,
            ('source_pitch_range', 'pr', getters.get_symbolic_pitch_range_string),
            ('target_octave_start_pitch', 'sp', getters.get_integer),
            )
