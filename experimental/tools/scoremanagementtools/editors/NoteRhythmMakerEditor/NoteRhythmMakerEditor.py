from abjad.tools import rhythmmakertools
from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools.editors.RhythmMakerEditor import RhythmMakerEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest


class NoteRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(rhythmmakertools.NoteRhythmMaker,
        )
