# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from scoremanager import getters
from scoremanager.editors.ListEditor import ListEditor


class OctaveTranspositionMappingInventoryEditor(ListEditor):
    r'''OctaveTranspositionMappingInventory editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import editors
        superclass = super(OctaveTranspositionMappingInventoryEditor, self)
        superclass.__init__(session=session, target=target)
        self._item_class = pitchtools.OctaveTranspositionMapping
        self._item_creator_class = editors.OctaveTranspositionMappingEditor
        self._item_editor_class = editors.OctaveTranspositionMappingEditor
        self._item_identifier = 'octave transposition mapping'

    ### PUBLIC PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        return systemtools.AttributeManifest(
            pitchtools.OctaveTranspositionMappingInventory,
            )