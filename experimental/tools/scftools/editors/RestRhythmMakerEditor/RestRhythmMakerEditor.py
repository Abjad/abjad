from abjad.tools import rhythmmakertools
from experimental.tools.scftools.editors.RhythmMakerEditor import RhythmMakerEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest
from experimental.tools.scftools import getters


class RestRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(rhythmmakertools.RestRhythmMaker,
        )
