from experimental.tools.scftools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scftools.editors.TargetManifest import TargetManifest
from experimental.tools.scftools.specifiers.PerformerSpecifier import PerformerSpecifier
from experimental.tools.scftools import selectors


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
