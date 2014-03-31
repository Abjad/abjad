# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class PitchRangeEditor(Editor):
    r'''PitchRange editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from abjad.tools import systemtools
        return systemtools.TargetManifest(
            pitchtools.PitchRange,
            (
                'one_line_named_pitch_repr', 
                'rp', 
                getters.get_symbolic_pitch_range_string,
                ),
            )