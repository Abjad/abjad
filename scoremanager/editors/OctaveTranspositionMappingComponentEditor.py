# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class OctaveTranspositionMappingComponentEditor(Editor):
    r'''OctaveTranspositionMappingComponent editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
    )
    
    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from scoremanager.editors import TargetManifest
        return TargetManifest(
            pitchtools.OctaveTranspositionMappingComponent,
            ('source_pitch_range', 'pr', getters.get_symbolic_pitch_range_string),
            ('target_octave_start_pitch', 'sp', getters.get_integer),
            )