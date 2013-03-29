from abjad.tools import contexttools
from scf import menuing
from scf.editors.ClefMarkEditor import ClefMarkEditor
from scf.editors.ObjectInventoryEditor import ObjectInventoryEditor
from scf.editors.TargetManifest import TargetManifest
from scf.editors.TempoMarkEditor import TempoMarkEditor


class ClefMarkInventoryEditor(ObjectInventoryEditor):

    ### CLASS ATTRIBUTES ###

    item_class = contexttools.ClefMark
    item_editor_class = ClefMarkEditor
    item_getter_configuration_method = menuing.UserInputGetter.append_clef
    item_identifier = 'clef mark'
    target_manifest = TargetManifest(contexttools.ClefMarkInventory,
        target_name_attribute='name',
        )
