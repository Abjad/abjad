# -*- encoding: utf-8 -*-
from experimental.tools import handlertools
from scoremanagertools import getters
from scoremanagertools.editors.DynamicHandlerEditor \
    import DynamicHandlerEditor


class NoteAndChordHairpinsHandlerEditor(DynamicHandlerEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            handlertools.NoteAndChordHairpinsHandler,
            ('hairpin_tokens', None, 'ht', getters.get_hairpin_tokens, True),
            ('minimum_duration', None, 'md', getters.get_duration, True),
            )
