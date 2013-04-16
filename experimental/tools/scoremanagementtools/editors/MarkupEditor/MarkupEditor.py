from abjad.tools import markuptools
from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools.editors.InteractiveEditor import InteractiveEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest


class MarkupEditor(InteractiveEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(markuptools.Markup,
        ('arg', 'contents_string', 'arg', 'ag', getters.get_string, True),
        ('direction', 'direction', 'dr', getters.get_direction_string, False),
        ('markup_name', 'name', 'nm', getters.get_string, False),
    )
