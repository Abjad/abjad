# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest
from experimental.tools.scoremanagertools.specifiers.PerformerSpecifier \
    import PerformerSpecifier
from experimental.tools.scoremanagertools import selectors


class PerformerSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS VARIABLES ###

    target_manifest = TargetManifest(
        PerformerSpecifier,
        ('performer', 'pf', selectors.Selector.make_performer_selector,)
        )

    ### PUBLIC PROPERTIES ###

    @property
    def target_name(self):
        try:
            return self.target.performer.name
        except AttributeError:
            pass
