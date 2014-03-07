# -*- encoding: utf-8 -*-
from experimental.tools import handlertools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class ReiteratedArticulationHandlerEditor(Editor):
    r'''ReiteratedArticulationHandler editor.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            handlertools.ReiteratedArticulationHandler,
            ('articulation_list', None, 'al', getters.get_articulations, False),
            ('minimum_duration', None, 'nd', getters.get_duration, False),
            ('maximum_duration', None, 'xd', getters.get_duration, False),
            ('minimum_written_pitch', None, 'np', 
                getters.get_named_pitch, False),
            ('maximum_written_pitch', None, 'xp', 
                getters.get_named_pitch, False),
            )
