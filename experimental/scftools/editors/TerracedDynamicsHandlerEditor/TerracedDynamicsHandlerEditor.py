from experimental.tools import handlertools
from scftools import getters
from scftools.editors.DynamicHandlerEditor import DynamicHandlerEditor
from scftools.editors.TargetManifest import TargetManifest


class TerracedDynamicsHandlerEditor(DynamicHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlertools.TerracedDynamicsHandler,
        ('dynamics', None, 'dy', getters.get_dynamics, True),
        ('minimum_duration', None, 'md', getters.get_duration, True),
    )
