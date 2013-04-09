from abjad.tools import rhythmmakertools
from scftools import getters
from scftools.editors.RhythmMakerEditor import RhythmMakerEditor
from scftools.editors.TargetManifest import TargetManifest


class NoteRhythmMakerEditor(RhythmMakerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(rhythmmakertools.NoteRhythmMaker,
        )
