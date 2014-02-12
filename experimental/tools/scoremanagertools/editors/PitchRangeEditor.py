# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class PitchRangeEditor(InteractiveEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return TargetManifest(
            pitchtools.PitchRange,
            ('one_line_named_pitch_repr', 'rp', 
                getters.get_symbolic_pitch_range_string),
            )
