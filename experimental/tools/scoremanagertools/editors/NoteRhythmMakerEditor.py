# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.RhythmMakerEditor \
    import RhythmMakerEditor


class NoteRhythmMakerEditor(RhythmMakerEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            rhythmmakertools.NoteRhythmMaker,
            )
