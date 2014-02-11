# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class ClefEditor(InteractiveEditor):

    ### CLASS VARIABLES ###

    target_manifest = TargetManifest(
        indicatortools.Clef,
        ('clef_name', 'nm', getters.get_string),
        )
