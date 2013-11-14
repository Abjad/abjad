# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from experimental.tools.scoremanagertools import iotools
from experimental.tools.scoremanagertools.editors.ClefEditor \
    import ClefEditor
from experimental.tools.scoremanagertools.editors.ObjectInventoryEditor \
    import ObjectInventoryEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest
from experimental.tools.scoremanagertools.editors.TempoEditor \
    import TempoEditor


class ClefInventoryEditor(ObjectInventoryEditor):

    ### CLASS VARIABLES ###

    item_class = marktools.Clef

    item_editor_class = ClefEditor

    item_getter_configuration_method = iotools.UserInputGetter.append_clef

    item_identifier = 'clef'

    target_manifest = TargetManifest(
        marktools.ClefInventory,
        target_name_attribute='name',
        )
