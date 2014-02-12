# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from scoremanagertools import getters
from scoremanagertools import wizards
from scoremanagertools.editors.ListEditor \
    import ListEditor
from scoremanagertools.editors.InstrumentEditor \
    import InstrumentEditor


class PerformerEditor(ListEditor):

    ### CLASS VARIABLES ###

    item_class = instrumenttools.Instrument

    item_creator_class = wizards.InstrumentCreationWizard

    item_creator_class_kwargs = {'is_ranged': True}

    item_editor_class = InstrumentEditor

    item_identifier = 'instrument'

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self.target.instruments

    @property
    def target_manifest(self):
        return self.TargetManifest(
            instrumenttools.Performer,
            ('name', 'nm', getters.get_string),
            target_attribute_name='name',
            )

    ### PUBLIC METHODS ###

    def initialize_target(self):
        if self.target is not None:
            return
        else:
            self.target = self.target_class()
