from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import specifiers
from experimental.tools.scoremanagertools.editors.ObjectInventoryEditor import ObjectInventoryEditor
from experimental.tools.scoremanagertools.editors.MusicContributionSpecifierEditor import MusicContributionSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest


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
