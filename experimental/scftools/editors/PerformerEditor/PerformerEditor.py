from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools.instrumenttools.Instrument import Instrument
from scftools import getters
from scftools import wizards
from scftools.editors.ListEditor import ListEditor
from scftools.editors.InstrumentEditor import InstrumentEditor
from scftools.editors.TargetManifest import TargetManifest


class PerformerEditor(ListEditor):

    ### CLASS ATTRIBUTES ###

    item_class = Instrument
    item_creator_class = wizards.InstrumentCreationWizard
    item_creator_class_kwargs = {'is_ranged': True}
    item_editor_class = InstrumentEditor
    item_identifier = 'instrument'
    target_manifest = TargetManifest(scoretools.Performer,
        ('name', 'nm', getters.get_string),
        target_attribute_name='name',
        )

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self.target.instruments

    ### PUBLIC METHODS ###

    def conditionally_initialize_target(self):
        if self.target is not None:
            return
        else:
            self.target = self.target_class()
