from experimental.tools import handlertools
from scftools import getters
from scftools.editors.DynamicHandlerEditor import DynamicHandlerEditor
from scftools.editors.TargetManifest import TargetManifest


class NoteAndChordHairpinsHandlerEditor(DynamicHandlerEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(handlertools.NoteAndChordHairpinsHandler,
        ('hairpin_tokens', None, 'ht', getters.get_hairpin_tokens, True),
        ('minimum_duration', None, 'md', getters.get_duration, True),
    )
