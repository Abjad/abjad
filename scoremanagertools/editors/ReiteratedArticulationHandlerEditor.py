# -*- encoding: utf-8 -*-
from experimental.tools import handlertools
from scoremanagertools import getters
from scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor


class ReiteratedArticulationHandlerEditor(InteractiveEditor):

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
