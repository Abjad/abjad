# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.ObjectInventoryEditor \
    import ObjectInventoryEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest
from experimental.tools.scoremanagertools.editors.TempoEditor \
    import TempoEditor
from experimental.tools.scoremanagertools.iotools.UserInputGetter \
    import UserInputGetter


class TempoInventoryEditor(ObjectInventoryEditor):

    ### CLASS VARIABLES ###

    item_class = indicatortools.Tempo

    item_editor_class = TempoEditor

    item_getter_configuration_method = UserInputGetter.append_tempo

    item_identifier = 'tempo'

    target_manifest = TargetManifest(
        indicatortools.TempoInventory,
        ('custom_identifier', 'custom_identifier', 'id', getters.get_string),
        target_name_attribute='inventory name',
        )

    ### PUBLIC PROPERTIES ###

    # TODO: abstract up to ObjectInventoryEditor?
    @property
    def target_summary_lines(self):
        result = []
        for item in self.target:
            result.append(repr(item))
        return result
