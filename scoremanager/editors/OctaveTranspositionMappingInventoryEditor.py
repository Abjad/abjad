# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from scoremanager import getters
from scoremanager.editors.ObjectInventoryEditor import ObjectInventoryEditor


class OctaveTranspositionMappingInventoryEditor(ObjectInventoryEditor):
    r'''OctaveTranspositionMappingInventory editor.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import editors
        superclass = super(OctaveTranspositionMappingInventoryEditor, self)
        superclass.__init__(session=session, target=target)
        self.item_class = pitchtools.OctaveTranspositionMapping
        self.item_creator_class = editors.OctaveTranspositionMappingEditor
        self.item_editor_class = editors.OctaveTranspositionMappingEditor
        self.item_identifier = 'octave transposition mapping'

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from scoremanager.editors import TargetManifest
        return TargetManifest(
            pitchtools.OctaveTranspositionMappingInventory,
            target_attribute_name='name',
            )
