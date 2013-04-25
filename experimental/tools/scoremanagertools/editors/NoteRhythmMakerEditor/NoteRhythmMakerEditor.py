from abjad.tools import rhythmmakertools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.RhythmMakerEditor import RhythmMakerEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest


class NoteRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(rhythmmakertools.NoteRhythmMaker,
        )
