# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from scoremanager import getters
from scoremanager.editors.ObjectInventoryEditor import ObjectInventoryEditor
from scoremanager.editors.MarkupEditor import MarkupEditor
from scoremanager.iotools.UserInputGetter import UserInputGetter


class MarkupInventoryEditor(ObjectInventoryEditor):

    ### CLASS VARIABLES ###

    item_class = markuptools.Markup

    item_creator_class = MarkupEditor

    item_editor_class = MarkupEditor

    item_identifier = 'markup'

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            markuptools.MarkupInventory,
            target_name_attribute='inventory name',
            )
