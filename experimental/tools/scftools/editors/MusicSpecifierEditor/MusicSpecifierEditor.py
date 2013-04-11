from experimental.tools.scftools import getters
from experimental.tools.scftools import specifiers
from experimental.tools.scftools.editors.ObjectInventoryEditor import ObjectInventoryEditor
from experimental.tools.scftools.editors.MusicContributionSpecifierEditor import MusicContributionSpecifierEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest


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
