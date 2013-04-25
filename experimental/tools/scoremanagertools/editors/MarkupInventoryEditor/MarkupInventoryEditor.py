from abjad.tools import contexttools
from abjad.tools import markuptools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.ObjectInventoryEditor import ObjectInventoryEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagertools.editors.MarkupEditor import MarkupEditor
from experimental.tools.scoremanagertools.menuing.UserInputGetter import UserInputGetter


class MarkupInventoryEditor(ObjectInventoryEditor):

    ### CLASS ATTRIBUTES ###

    item_class = markuptools.Markup
    item_creator_class = MarkupEditor
    item_editor_class = MarkupEditor
    item_identifier = 'markup'
    target_manifest = TargetManifest(markuptools.MarkupInventory,
        ('name', 'name', 'nm', getters.get_string),
        target_name_attribute='inventory name',
        )

    ### READ-ONLY PUBLIC PROPERTIES ###

    # TODO: abstract up to ObjectInventoryEditor?
    @property
    def target_summary_lines(self):
        result = []
        for item in self.target:
            label = item.markup_name or 'anonymous'
            result.append('{}: {}'.format(label, item.lilypond_format))
        return result
