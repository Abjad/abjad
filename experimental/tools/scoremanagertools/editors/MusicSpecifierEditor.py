# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import specifiers
from experimental.tools.scoremanagertools.editors.ObjectInventoryEditor \
    import ObjectInventoryEditor
from experimental.tools.scoremanagertools.editors.MusicContributionSpecifierEditor \
    import MusicContributionSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class MusicSpecifierEditor(ObjectInventoryEditor):

    ### CLASS VARIABLES ###

    item_class = specifiers.MusicContributionSpecifier

    item_creator_class = MusicContributionSpecifierEditor

    item_editor_class = MusicContributionSpecifierEditor

    item_identifier = 'music contribution'

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return TargetManifest(
            specifiers.MusicSpecifier,
            )
