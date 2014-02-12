# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class ClefEditor(InteractiveEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return TargetManifest(
            indicatortools.Clef,
            ('clef_name', 'nm', getters.get_string),
            )
