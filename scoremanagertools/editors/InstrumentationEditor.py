# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from scoremanagertools import getters
from scoremanagertools import wizards
from scoremanagertools.editors.ListEditor \
    import ListEditor
from scoremanagertools.editors.PerformerEditor \
    import PerformerEditor


class InstrumentationEditor(ListEditor):

    ### CLASS VARIABLES ###

    item_class = instrumenttools.Performer

    item_creator_class = wizards.PerformerCreationWizard

    item_creator_class_kwargs = {'is_ranged': True}

    item_editor_class = PerformerEditor

    item_identifier = 'performer'

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return self.target_name or 'instrumentation'

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self.target.performers

    @property
    def target_manifest(self):
        return self.TargetManifest(
            instrumenttools.InstrumentationSpecifier,
            )

