# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from scoremanager import getters
from scoremanager.editors.RhythmMakerEditor import RhythmMakerEditor


class NoteRhythmMakerEditor(RhythmMakerEditor):
    r'''NoteRhythmMaker editor.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            rhythmmakertools.NoteRhythmMaker,
            )
