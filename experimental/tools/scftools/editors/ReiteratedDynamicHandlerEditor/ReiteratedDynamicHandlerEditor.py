from experimental.tools import handlertools
from experimental.tools.scftools import getters
from experimental.tools.scftools.editors.DynamicHandlerEditor import DynamicHandlerEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest


class ReiteratedDynamicHandlerEditor(DynamicHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlertools.ReiteratedDynamicHandler,
        ('dynamic_name', None, 'dy', getters.get_dynamic, True),
        ('minimum_duration', None, 'md', getters.get_duration, True),
    )
