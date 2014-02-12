# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from scoremanagertools import getters
from scoremanagertools.editors.ObjectInventoryEditor \
    import ObjectInventoryEditor
from scoremanagertools.editors.OctaveTranspositionMappingComponentEditor \
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
            ('custom_identifier', 'custom_identifier', 'id', getters.get_string),
            target_name_attribute='name',
            )
