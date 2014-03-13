# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class PitchRangeEditor(Editor):
    r'''PitchRange editor.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        from editors import TargetManifest
        return TargetManifest(
            pitchtools.PitchRange,
            ('one_line_named_pitch_repr', 'rp', 
                getters.get_symbolic_pitch_range_string),
            )
