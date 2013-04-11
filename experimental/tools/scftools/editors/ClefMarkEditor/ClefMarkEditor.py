from abjad.tools import contexttools
from experimental.tools.scftools import getters
from experimental.tools.scftools.editors.InteractiveEditor import InteractiveEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest


class ClefMarkEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(contexttools.ClefMark,
        ('clef_name', 'nm', getters.get_string),
        )
