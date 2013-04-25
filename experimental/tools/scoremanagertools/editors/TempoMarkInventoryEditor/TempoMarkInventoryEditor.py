from abjad.tools import contexttools
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools.editors.ObjectInventoryEditor import ObjectInventoryEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagertools.editors.TempoMarkEditor import TempoMarkEditor
from experimental.tools.scoremanagertools.menuing.UserInputGetter import UserInputGetter


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
