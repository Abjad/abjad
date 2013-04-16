from abjad.tools import scoretools
from experimental.tools.scoremanagementtools import getters
from experimental.tools.scoremanagementtools import wizards
from experimental.tools.scoremanagementtools.editors.ListEditor import ListEditor
from experimental.tools.scoremanagementtools.editors.PerformerEditor import PerformerEditor
from experimental.tools.scoremanagementtools.editors.TargetManifest import TargetManifest


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
