# -*- encoding: utf-8 -*-
from experimental.tools import handlertools
from scoremanagertools import getters
from scoremanagertools.editors.DynamicHandlerEditor \
    import DynamicHandlerEditor


class NoteAndChordHairpinHandlerEditor(DynamicHandlerEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            handlertools.NoteAndChordHairpinHandler,
            ('hairpin_token', None, 'ht', getters.get_hairpin_token, True),
            ('minimum_duration', None, 'md', getters.get_duration, True),
            )
