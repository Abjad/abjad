# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.specifiers.PerformerSpecifier \
    import PerformerSpecifier
from experimental.tools.scoremanagertools import iotools


class PerformerSpecifierEditor(ParameterSpecifierEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            PerformerSpecifier,
            ('performer', 'pf', iotools.Selector.make_performer_selector,)
            )

    @property
    def target_name(self):
        try:
            return self.target.performer.name
        except AttributeError:
            pass
