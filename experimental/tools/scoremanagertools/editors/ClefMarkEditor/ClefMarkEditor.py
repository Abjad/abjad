from abjad.tools import contexttools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.InteractiveEditor import InteractiveEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest


class ClefMarkEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(contexttools.ClefMark,
        ('clef_name', 'nm', getters.get_string),
        )
