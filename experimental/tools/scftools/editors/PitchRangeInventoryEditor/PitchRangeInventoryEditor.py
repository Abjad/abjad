from abjad.tools import pitchtools
from experimental.tools.scftools.editors.InteractiveEditor import InteractiveEditor
from experimental.tools.scftools.editors.ObjectInventoryEditor import ObjectInventoryEditor
from experimental.tools.scftools.editors.PitchRangeEditor import PitchRangeEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest
from experimental.tools.scftools.menuing.UserInputGetter import UserInputGetter


class PitchRangeInventoryEditor(ObjectInventoryEditor):

    ### CLASS ATTRIBUTES ###

    item_getter_configuration_method = UserInputGetter.append_symbolic_pitch_range_string
    item_class = pitchtools.PitchRange
    item_editor_class = PitchRangeEditor
    item_identifier = 'pitch range'
    target_manifest = TargetManifest(pitchtools.PitchRangeInventory,
        target_name_attribute='name',
        )

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def target_summary_lines(self):
        result = []
        for pitch_range in self.target:
            result.append(repr(pitch_range))
        return result
