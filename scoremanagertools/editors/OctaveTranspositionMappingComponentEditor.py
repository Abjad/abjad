# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from scoremanagertools import getters
from scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor


class OctaveTranspositionMappingComponentEditor(InteractiveEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            pitchtools.OctaveTranspositionMappingComponent,
            ('source_pitch_range', 'pr', getters.get_symbolic_pitch_range_string),
            ('target_octave_start_pitch', 'sp', getters.get_integer),
            )
