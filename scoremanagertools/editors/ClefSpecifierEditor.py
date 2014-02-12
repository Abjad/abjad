# -*- encoding: utf-8 -*-
from scoremanagertools import iotools
from scoremanagertools.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor


class ClefSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS VARIABLES ###

    @property
    def target_manifest(self):
        from scoremanagertools import specifiers
        return self.TargetManifest(
            specifiers.ClefSpecifier,
            ('clef_name', 'cf', iotools.Selector.make_clef_name_selector),
            )
