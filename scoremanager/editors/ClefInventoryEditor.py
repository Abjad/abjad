# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from scoremanager import iotools
from scoremanager.editors.ObjectInventoryEditor import ObjectInventoryEditor


class ClefInventoryEditor(ObjectInventoryEditor):
    r'''Clef inventory editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
    )
    
    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import editors
        superclass = super(ClefInventoryEditor, self)
        superclass.__init__(session=session, target=target)
        self._item_class = indicatortools.Clef
        self._item_editor_class = editors.ClefEditor
        self._item_getter_configuration_method = \
            iotools.UserInputGetter.append_clef
        self._item_identifier = 'clef'

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from scoremanager.editors import TargetManifest
        return TargetManifest(
            indicatortools.ClefInventory,
            target_name_attribute='name',
            )