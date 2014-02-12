# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from experimental.tools.scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor
from experimental.tools.scoremanagertools.editors.ObjectInventoryEditor \
    import ObjectInventoryEditor
from experimental.tools.scoremanagertools.editors.PitchRangeEditor \
    import PitchRangeEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest
from experimental.tools.scoremanagertools.iotools.UserInputGetter \
    import UserInputGetter


class PitchRangeInventoryEditor(ObjectInventoryEditor):

    ### CLASS VARIABLES ###

    item_getter_configuration_method = \
        UserInputGetter.append_symbolic_pitch_range_string

    item_class = pitchtools.PitchRange

    item_editor_class = PitchRangeEditor

    item_identifier = 'pitch range'

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return TargetManifest(
            pitchtools.PitchRangeInventory,
            target_name_attribute='name',
            )

    @property
    def target_summary_lines(self):
        result = []
        for pitch_range in self.target:
            result.append(repr(pitch_range))
        return result
