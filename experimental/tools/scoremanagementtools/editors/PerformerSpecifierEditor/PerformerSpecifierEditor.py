from experimental.tools.scoremanagementtools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagementtools.specifiers.PerformerSpecifier import PerformerSpecifier
from experimental.tools.scoremanagementtools import selectors


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
