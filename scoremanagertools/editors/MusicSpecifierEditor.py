# -*- encoding: utf-8 -*-
from scoremanagertools import getters
from scoremanagertools import specifiers
from scoremanagertools.editors.ObjectInventoryEditor \
    import ObjectInventoryEditor
from scoremanagertools.editors.MusicContributionSpecifierEditor \
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
        from scoremanagertools import specifiers
        return self.TargetManifest(
            specifiers.MusicSpecifier,
            )
