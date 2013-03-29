from abjad.tools import scoretools
from scf import getters
from scf import wizards
from scf.editors.ListEditor import ListEditor
from scf.editors.PerformerEditor import PerformerEditor
from scf.editors.TargetManifest import TargetManifest


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
