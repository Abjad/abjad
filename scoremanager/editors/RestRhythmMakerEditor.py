# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from scoremanager import getters
from scoremanager.editors.RhythmMakerEditor import RhythmMakerEditor


class RestRhythmMakerEditor(RhythmMakerEditor):
    r'''RestRhythmMaker editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from scoremanager import editors
        return editors.TargetManifest(
            rhythmmakertools.RestRhythmMaker,
            )