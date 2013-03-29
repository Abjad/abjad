from abjad.tools import contexttools
from scf import getters
from scf.editors.InteractiveEditor import InteractiveEditor
from scf.editors.TargetManifest import TargetManifest


class ClefMarkEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(contexttools.ClefMark,
        ('clef_name', 'nm', getters.get_string),
        )
