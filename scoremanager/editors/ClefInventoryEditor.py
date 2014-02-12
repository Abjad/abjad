# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from scoremanager import iotools
from scoremanager.editors.ClefEditor import ClefEditor
from scoremanager.editors.ObjectInventoryEditor import ObjectInventoryEditor


class ClefInventoryEditor(ObjectInventoryEditor):

    ### CLASS VARIABLES ###

    item_class = indicatortools.Clef

    item_editor_class = ClefEditor

    item_getter_configuration_method = iotools.UserInputGetter.append_clef

    item_identifier = 'clef'

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            indicatortools.ClefInventory,
            target_name_attribute='name',
            )
