from abjad.tools import pitchtools
from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools.editors.ObjectInventoryEditor import ObjectInventoryEditor
from experimental.tools.scoremanagementtools.editors.OctaveTranspositionMappingComponentEditor import OctaveTranspositionMappingComponentEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest


class OctaveTranspositionMappingEditor(ObjectInventoryEditor):

    ### CLASS ATTRIBUTES ###

    item_class = pitchtools.OctaveTranspositionMappingComponent
    item_creator_class = OctaveTranspositionMappingComponentEditor
    item_editor_class = OctaveTranspositionMappingComponentEditor
    item_identifier = 'octave transposition mapping component'
    target_manifest = TargetManifest(pitchtools.OctaveTranspositionMapping,
        ('name', 'name', 'nm', getters.get_string),
        target_name_attribute='name',
        )
