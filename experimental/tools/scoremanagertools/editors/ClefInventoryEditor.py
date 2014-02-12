# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from experimental.tools.scoremanagertools import iotools
from experimental.tools.scoremanagertools.editors.ClefEditor \
    import ClefEditor
from experimental.tools.scoremanagertools.editors.ObjectInventoryEditor \
    import ObjectInventoryEditor


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
