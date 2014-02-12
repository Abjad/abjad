# -*- encoding: utf-8 -*-
from scoremanager import iotools
from scoremanager.editors.SpecifierEditor import SpecifierEditor


class ClefSpecifierEditor(SpecifierEditor):

    ### CLASS VARIABLES ###

    @property
    def target_manifest(self):
        from scoremanager import specifiers
        return self.TargetManifest(
            specifiers.ClefSpecifier,
            ('clef_name', 'cf', iotools.Selector.make_clef_name_selector),
            )
