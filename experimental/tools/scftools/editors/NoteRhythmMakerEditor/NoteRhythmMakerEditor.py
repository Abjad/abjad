from abjad.tools import rhythmmakertools
from experimental.tools.scftools import getters
from experimental.tools.scftools.editors.RhythmMakerEditor import RhythmMakerEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest


class NoteRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(rhythmmakertools.NoteRhythmMaker,
        )
