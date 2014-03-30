# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class MarkupEditor(Editor):
    r'''Markup editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )
    
    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from scoremanager import editors
        return editors.TargetManifest(
            markuptools.Markup,
            ('arg', 'contents_string', 'arg', 'ag', getters.get_string, True),
            ('direction', 'direction', 'dr', getters.get_direction_string, False),
            )