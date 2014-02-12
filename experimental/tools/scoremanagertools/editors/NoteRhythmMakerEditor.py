# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.RhythmMakerEditor \
    import RhythmMakerEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class NoteRhythmMakerEditor(RhythmMakerEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return TargetManifest(
            rhythmmakertools.NoteRhythmMaker,
            )
