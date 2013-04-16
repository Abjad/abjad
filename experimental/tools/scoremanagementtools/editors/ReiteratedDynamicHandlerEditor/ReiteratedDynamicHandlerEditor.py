from experimental.tools import handlertools
from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools.editors.DynamicHandlerEditor import DynamicHandlerEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest


class ReiteratedDynamicHandlerEditor(DynamicHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlertools.ReiteratedDynamicHandler,
        ('dynamic_name', None, 'dy', getters.get_dynamic, True),
        ('minimum_duration', None, 'md', getters.get_duration, True),
    )
