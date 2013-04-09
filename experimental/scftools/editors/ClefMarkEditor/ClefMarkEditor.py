from abjad.tools import contexttools
from scftools import getters
from scftools.editors.InteractiveEditor import InteractiveEditor
from scftools.editors.TargetManifest import TargetManifest


class ClefMarkEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(contexttools.ClefMark,
        ('clef_name', 'nm', getters.get_string),
        )
