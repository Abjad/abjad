from abjad.tools import pitchtools
from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools.editors.ObjectInventoryEditor import ObjectInventoryEditor
from experimental.tools.scoremanagementtools.editors.OctaveTranspositionMappingEditor import OctaveTranspositionMappingEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest


class OctaveTranspositionMappingInventoryEditor(ObjectInventoryEditor):

    ### CLASS ATTRIBUTES ###

    item_class = pitchtools.OctaveTranspositionMapping
    item_creator_class = OctaveTranspositionMappingEditor
    item_editor_class = OctaveTranspositionMappingEditor
    item_identifier = 'octave transposition mapping'
    target_manifest = TargetManifest(pitchtools.OctaveTranspositionMappingInventory,
        ('name', 'name', 'nm', getters.get_string),
        target_attribute_name='name',
        )
