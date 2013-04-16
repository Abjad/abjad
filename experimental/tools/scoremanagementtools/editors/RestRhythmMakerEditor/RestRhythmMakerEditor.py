from abjad.tools import rhythmmakertools
from experimental.tools.scoremanagementtools.editors.RhythmMakerEditor import RhythmMakerEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagementtools import getters


class RestRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(rhythmmakertools.RestRhythmMaker,
        )
