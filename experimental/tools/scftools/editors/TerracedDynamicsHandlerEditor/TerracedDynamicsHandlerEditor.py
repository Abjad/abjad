from experimental.tools import handlertools
from experimental.tools.scftools import getters
from experimental.tools.scftools.editors.DynamicHandlerEditor import DynamicHandlerEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest


class TerracedDynamicsHandlerEditor(DynamicHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlertools.TerracedDynamicsHandler,
        ('dynamics', None, 'dy', getters.get_dynamics, True),
        ('minimum_duration', None, 'md', getters.get_duration, True),
    )
