from abjad.tools import scoretools
from scftools import getters
from scftools import wizards
from scftools.editors.ListEditor import ListEditor
from scftools.editors.PerformerEditor import PerformerEditor
from scftools.editors.TargetManifest import TargetManifest


class InstrumentationEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    item_class = scoretools.Performer
    item_creator_class = wizards.PerformerCreationWizard
    item_creator_class_kwargs = {'is_ranged': True}
    item_editor_class = PerformerEditor
    item_identifier = 'performer'
    target_manifest = TargetManifest(scoretools.InstrumentationSpecifier,
        )

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return self.target_name or 'performers'

    @property
    def items(self):
        return self.target.performers
