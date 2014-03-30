# -*- encoding: utf-8 -*-
from experimental.tools import handlertools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class NoteAndChordHairpinsHandlerEditor(Editor):
    r'''NoteAndChordHairpinsHandler editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )
    
    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from abjad.tools import systemtools
        return systemtools.TargetManifest(
            handlertools.NoteAndChordHairpinsHandler,
            ('hairpin_tokens', None, 'ht', getters.get_hairpin_tokens, True),
            ('minimum_duration', None, 'md', getters.get_duration, True),
            )