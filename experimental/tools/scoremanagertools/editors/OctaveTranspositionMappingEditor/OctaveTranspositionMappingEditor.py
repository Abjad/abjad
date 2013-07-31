# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.ObjectInventoryEditor \
    import ObjectInventoryEditor
from experimental.tools.scoremanagertools.editors.OctaveTranspositionMappingComponentEditor \
    import OctaveTranspositionMappingComponentEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class OctaveTranspositionMappingEditor(ObjectInventoryEditor):

    ### CLASS VARIABLES ###

    item_class = pitchtools.OctaveTranspositionMappingComponent

    item_creator_class = OctaveTranspositionMappingComponentEditor

    item_editor_class = OctaveTranspositionMappingComponentEditor

    item_identifier = 'octave transposition mapping component'

    target_manifest = TargetManifest(
        pitchtools.OctaveTranspositionMapping,
        ('name', 'name', 'nm', getters.get_string),
        target_name_attribute='name',
        )
