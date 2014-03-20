# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from scoremanager import getters
from scoremanager.editors.RhythmMakerEditor import RhythmMakerEditor


class RestRhythmMakerEditor(RhythmMakerEditor):
    r'''RestRhythmMaker editor.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from scoremanager.editors import TargetManifest
        return TargetManifest(
            rhythmmakertools.RestRhythmMaker,
            )
