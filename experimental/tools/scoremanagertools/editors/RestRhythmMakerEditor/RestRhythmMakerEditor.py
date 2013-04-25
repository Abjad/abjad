from abjad.tools import rhythmmakertools
from experimental.tools.scoremanagertools.editors.RhythmMakerEditor import RhythmMakerEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagertools import getters


class RestRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(rhythmmakertools.RestRhythmMaker,
        )
