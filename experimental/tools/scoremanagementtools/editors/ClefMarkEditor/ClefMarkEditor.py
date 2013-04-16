from abjad.tools import contexttools
from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools.editors.InteractiveEditor import InteractiveEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest


class ClefMarkEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(contexttools.ClefMark,
        ('clef_name', 'nm', getters.get_string),
        )
