# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from scoremanager import getters
from scoremanager.editors.ObjectInventoryEditor import ObjectInventoryEditor
from scoremanager.editors.OctaveTranspositionMappingComponentEditor \
    import OctaveTranspositionMappingComponentEditor


class OctaveTranspositionMappingEditor(ObjectInventoryEditor):

    ### CLASS VARIABLES ###

    item_class = pitchtools.OctaveTranspositionMappingComponent

    item_creator_class = OctaveTranspositionMappingComponentEditor

    item_editor_class = OctaveTranspositionMappingComponentEditor

    item_identifier = 'octave transposition mapping component'

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            pitchtools.OctaveTranspositionMapping,
            target_name_attribute='name',
            )
