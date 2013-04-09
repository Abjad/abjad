from experimental.tools import handlertools
from scftools import getters
from scftools.editors.DynamicHandlerEditor import DynamicHandlerEditor
from scftools.editors.TargetManifest import TargetManifest


class ReiteratedDynamicHandlerEditor(DynamicHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlertools.ReiteratedDynamicHandler,
        ('dynamic_name', None, 'dy', getters.get_dynamic, True),
        ('minimum_duration', None, 'md', getters.get_duration, True),
    )
