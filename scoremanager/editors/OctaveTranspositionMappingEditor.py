# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from scoremanager import getters
from scoremanager.editors.ObjectInventoryEditor import ObjectInventoryEditor


class OctaveTranspositionMappingEditor(ObjectInventoryEditor):
    r'''OctaveTranspositionMapping editor.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import editors
        superclass = super(OctaveTranspositionMappingEditor, self)
        superclass.__init__(session=session, target=target)
        self.item_class = pitchtools.OctaveTranspositionMappingComponent
        self.item_creator_class = \
            editors.OctaveTranspositionMappingComponentEditor
        self.item_editor_class = \
            editors.OctaveTranspositionMappingComponentEditor
        self.item_identifier = 'octave transposition mapping component'

    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from editors import TargetManifest
        return TargetManifest(
            pitchtools.OctaveTranspositionMapping,
            target_name_attribute='name',
            )
