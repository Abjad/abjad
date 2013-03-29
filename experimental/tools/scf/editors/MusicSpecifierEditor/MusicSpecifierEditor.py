from scf import getters
from scf import specifiers
from scf.editors.ObjectInventoryEditor import ObjectInventoryEditor
from scf.editors.MusicContributionSpecifierEditor import MusicContributionSpecifierEditor
from scf.editors.TargetManifest import TargetManifest


class MusicSpecifierEditor(ObjectInventoryEditor):

    ### CLASS ATTRIBUTES ###

    item_class = specifiers.MusicContributionSpecifier
    item_creator_class = MusicContributionSpecifierEditor
    item_editor_class = MusicContributionSpecifierEditor
    item_identifier = 'music contribution'
    target_manifest = TargetManifest(specifiers.MusicSpecifier,
        #('name', 'name', 'nm', getters.get_string, False),
        #target_attribute_name='name',
        )
