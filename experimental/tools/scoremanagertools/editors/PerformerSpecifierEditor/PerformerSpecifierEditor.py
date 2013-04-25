from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagertools.specifiers.PerformerSpecifier import PerformerSpecifier
from experimental.tools.scoremanagertools import selectors


class PerformerSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(PerformerSpecifier,
        ('performer', 'pf', selectors.PerformerSelector),
        )

    ### READ-ONLY PROPERTIES ###

    @property
    def target_name(self):
        try:
            return self.target.performer.name
        except AttributeError:
            pass
