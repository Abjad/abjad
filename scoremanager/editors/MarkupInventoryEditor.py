# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from scoremanager import getters
from scoremanager.editors.ObjectInventoryEditor import ObjectInventoryEditor


class MarkupInventoryEditor(ObjectInventoryEditor):
    r'''Markup inventory editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )
    
    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import editors
        superclass = super(MarkupInventoryEditor, self)
        superclass.__init__(session=session, target=target)
        self._item_class = markuptools.Markup
        self._item_creator_class = editors.MarkupEditor
        self._item_editor_class = editors.MarkupEditor
        self._item_identifier = 'markup'

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from abjad.tools import systemtools
        return systemtools.TargetManifest(
            markuptools.MarkupInventory,
            target_name_attribute='inventory name',
            )