# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from scoremanager import iotools
from scoremanager.editors.ListEditor import ListEditor


class ClefInventoryEditor(ListEditor):
    r'''Clef inventory editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )
    
    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        superclass = super(ClefInventoryEditor, self)
        superclass.__init__(session=session, target=target)
        self._item_class = indicatortools.Clef
        self._item_getter_configuration_method = \
            iotools.UserInputGetter.append_clef
        # TODO: derive _item_identifier from _item_class?
        self._item_identifier = 'clef'

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from abjad.tools import systemtools
        return systemtools.TargetManifest(
            indicatortools.ClefInventory,
            target_name_attribute='name',
            )