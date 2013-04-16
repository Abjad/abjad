from experimental.tools import handlertools
from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools.editors.DynamicHandlerEditor import DynamicHandlerEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest


class TerracedDynamicsHandlerEditor(DynamicHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlertools.TerracedDynamicsHandler,
        ('dynamics', None, 'dy', getters.get_dynamics, True),
        ('minimum_duration', None, 'md', getters.get_duration, True),
    )
