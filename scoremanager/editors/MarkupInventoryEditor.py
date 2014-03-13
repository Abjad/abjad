# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from scoremanager import getters
from scoremanager.editors.ObjectInventoryEditor import ObjectInventoryEditor


class MarkupInventoryEditor(ObjectInventoryEditor):
    r'''Markup inventory editor.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import editors
        superclass = super(MarkupInventoryEditor, self)
        superclass.__init__(session=session, target=target)
        self.item_class = markuptools.Markup
        self.item_creator_class = editors.MarkupEditor
        self.item_editor_class = editors.MarkupEditor
        self.item_identifier = 'markup'

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        from editors import TargetManifest
        return TargetManifest(
            markuptools.MarkupInventory,
            target_name_attribute='inventory name',
            )
