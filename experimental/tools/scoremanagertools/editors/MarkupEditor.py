# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor


class MarkupEditor(InteractiveEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            markuptools.Markup,
            ('arg', 'contents_string', 'arg', 'ag', getters.get_string, True),
            ('direction', 'direction', 'dr', getters.get_direction_string, False),
            ('markup_name', 'name', 'nm', getters.get_string, False),
            )
