from experimental.tools import handlertools
from experimental.tools.scftools import getters
from experimental.tools.scftools.editors.DynamicHandlerEditor import DynamicHandlerEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest


class NoteAndChordHairpinHandlerEditor(DynamicHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlertools.NoteAndChordHairpinHandler,
        ('hairpin_token', None, 'ht', getters.get_hairpin_token, True),
        ('minimum_duration', None, 'md', getters.get_duration, True),
    )
