from abjad.tools import contexttools
from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools.editors.ObjectInventoryEditor import ObjectInventoryEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagementtools.editors.TempoMarkEditor import TempoMarkEditor
from experimental.tools.scoremanagementtools.menuing.UserInputGetter import UserInputGetter


class TempoMarkInventoryEditor(ObjectInventoryEditor):

    ### CLASS ATTRIBUTES ###

    item_class = contexttools.TempoMark
    item_editor_class = TempoMarkEditor
    item_getter_configuration_method = UserInputGetter.append_tempo
    item_identifier = 'tempo mark'
    target_manifest = TargetManifest(contexttools.TempoMarkInventory,
        ('name', 'name', 'nm', getters.get_string),
        target_name_attribute='inventory name',
        )

    ### READ-ONLY PUBLIC PROPERTIES ###

    # TODO: abstract up to ObjectInventoryEditor?
    @property
    def target_summary_lines(self):
        result = []
        for item in self.target:
            result.append(repr(item))
        return result
