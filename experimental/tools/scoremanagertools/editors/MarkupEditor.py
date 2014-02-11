# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class MarkupEditor(InteractiveEditor):

    ### CLASS VARIABLES ###

    target_manifest = TargetManifest(
        markuptools.Markup,
        ('arg', 'contents_string', 'arg', 'ag', getters.get_string, True),
        ('direction', 'direction', 'dr', getters.get_direction_string, False),
        ('markup_name', 'name', 'nm', getters.get_string, False),
    )
