from abjad.tools import pitchtools
from scf import getters
from scf.editors.ObjectInventoryEditor import ObjectInventoryEditor
from scf.editors.OctaveTranspositionMappingComponentEditor import OctaveTranspositionMappingComponentEditor
from scf.editors.TargetManifest import TargetManifest


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
