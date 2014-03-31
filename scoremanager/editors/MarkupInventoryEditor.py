# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from scoremanager import getters
from scoremanager.editors.ListEditor import ListEditor


class MarkupInventoryEditor(ListEditor):
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
        # TODO: derive from self._item_class?
        self._item_identifier = 'markup'

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from abjad.tools import systemtools
        return systemtools.TargetManifest(
            markuptools.MarkupInventory,
            target_name_attribute='inventory name',
            )