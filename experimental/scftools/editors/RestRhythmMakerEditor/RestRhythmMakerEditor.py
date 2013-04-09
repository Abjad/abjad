from abjad.tools import rhythmmakertools
from scftools.editors.RhythmMakerEditor import RhythmMakerEditor
from scftools.editors.TargetManifest import TargetManifest
from scftools import getters


class RestRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(rhythmmakertools.RestRhythmMaker,
        )
