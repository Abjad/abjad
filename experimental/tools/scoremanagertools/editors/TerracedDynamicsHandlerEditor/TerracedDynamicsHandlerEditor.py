from experimental.tools import handlertools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.DynamicHandlerEditor import DynamicHandlerEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest


class TerracedDynamicsHandlerEditor(DynamicHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlertools.TerracedDynamicsHandler,
        ('dynamics', None, 'dy', getters.get_dynamics, True),
        ('minimum_duration', None, 'md', getters.get_duration, True),
    )
