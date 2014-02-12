# -*- encoding: utf-8 -*-
from experimental.tools import handlertools
from scoremanagertools import getters
from scoremanagertools.editors.DynamicHandlerEditor \
    import DynamicHandlerEditor


class TerracedDynamicsHandlerEditor(DynamicHandlerEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            handlertools.TerracedDynamicsHandler,
            ('dynamics', None, 'dy', getters.get_dynamics, True),
            ('minimum_duration', None, 'md', getters.get_duration, True),
            )
