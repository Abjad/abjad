from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools import specifiers
from experimental.tools.scoremanagementtools.editors.ObjectInventoryEditor import ObjectInventoryEditor
from experimental.tools.scoremanagementtools.editors.MusicContributionSpecifierEditor import MusicContributionSpecifierEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest


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
