# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from scoremanager import getters
from scoremanager.editors.ObjectInventoryEditor import ObjectInventoryEditor
from scoremanager.editors.TempoEditor import TempoEditor
from scoremanager.iotools.UserInputGetter import UserInputGetter


class TempoInventoryEditor(ObjectInventoryEditor):
    r'''TempoInventory editor.
    '''

    ### CLASS VARIABLES ###

    item_class = indicatortools.Tempo

    item_editor_class = TempoEditor

    item_getter_configuration_method = UserInputGetter.append_tempo

    item_identifier = 'tempo'

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            indicatortools.TempoInventory,
            target_name_attribute='inventory name',
            )
