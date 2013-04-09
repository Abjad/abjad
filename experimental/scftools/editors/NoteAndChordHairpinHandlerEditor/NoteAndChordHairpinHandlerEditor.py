from experimental.tools import handlertools
from scftools import getters
from scftools.editors.DynamicHandlerEditor import DynamicHandlerEditor
from scftools.editors.TargetManifest import TargetManifest


class NoteAndChordHairpinHandlerEditor(DynamicHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlertools.NoteAndChordHairpinHandler,
        ('hairpin_token', None, 'ht', getters.get_hairpin_token, True),
        ('minimum_duration', None, 'md', getters.get_duration, True),
    )
