# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import iotools
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest
from experimental.tools.scoremanagertools.specifiers.ClefSpecifier \
    import ClefSpecifier


class ClefSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS VARIABLES ###

    @property
    def target_manifest(self):
        return TargetManifest(
            ClefSpecifier,
            ('clef_name', 'cf', iotools.Selector.make_clef_name_selector),
            )
