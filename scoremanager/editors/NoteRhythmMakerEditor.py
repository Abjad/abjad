# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class NoteRhythmMakerEditor(Editor):
    r'''NoteRhythmMaker editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )
    
    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from abjad.tools import systemtools
        return systemtools.TargetManifest(
            rhythmmakertools.NoteRhythmMaker,
            )