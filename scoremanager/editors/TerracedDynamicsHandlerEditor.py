# -*- encoding: utf-8 -*-
from experimental.tools import handlertools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class TerracedDynamicsHandlerEditor(Editor):
    r'''TerracedDynamicsHandler editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from abjad.tools import systemtools
        return systemtools.TargetManifest(
            handlertools.TerracedDynamicsHandler,
            ('dynamics', None, 'dy', getters.get_dynamics, True),
            ('minimum_duration', None, 'md', getters.get_duration, True),
            )