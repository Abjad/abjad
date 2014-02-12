# -*- encoding: utf-8 -*-
from scoremanager import getters
from scoremanager import specifiers
from scoremanager.editors.ObjectInventoryEditor \
    import ObjectInventoryEditor
from scoremanager.editors.MusicContributionSpecifierEditor \
    import MusicContributionSpecifierEditor


class MusicSpecifierEditor(ObjectInventoryEditor):

    ### CLASS VARIABLES ###

    item_class = specifiers.MusicContributionSpecifier

    item_creator_class = MusicContributionSpecifierEditor

    item_editor_class = MusicContributionSpecifierEditor

    item_identifier = 'music contribution'

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        from scoremanager import specifiers
        return self.TargetManifest(
            specifiers.MusicSpecifier,
            )
