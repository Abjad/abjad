# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class ClefEditor(Editor):
    r'''Clef editor.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from editors import TargetManifest
        return TargetManifest(
            indicatortools.Clef,
            ('clef_name', 'nm', getters.get_string),
            )
