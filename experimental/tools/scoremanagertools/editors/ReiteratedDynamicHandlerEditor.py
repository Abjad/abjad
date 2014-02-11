# -*- encoding: utf-8 -*-
from experimental.tools import handlertools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.DynamicHandlerEditor \
    import DynamicHandlerEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class ReiteratedDynamicHandlerEditor(DynamicHandlerEditor):

    ### CLASS VARIABLES ###

    target_manifest = TargetManifest(
        handlertools.ReiteratedDynamicHandler,
        ('dynamic_name', None, 'dy', getters.get_dynamic, True),
        ('minimum_duration', None, 'md', getters.get_duration, True),
    )
