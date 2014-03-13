# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from scoremanager import getters
from scoremanager import wizards
from scoremanager.editors.ListEditor import ListEditor


class PerformerEditor(ListEditor):
    r'''Performer editor.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import editors
        superclass = super(PerformerEditor, self)
        superclass.__init__(session=session, target=target)
        self.item_class = instrumenttools.Instrument
        self.item_creator_class = wizards.InstrumentCreationWizard
        self.item_creator_class_kwargs = {'is_ranged': True}
        self.item_editor_class = editors.InstrumentEditor
        self.item_identifier = 'instrument'


    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self.target.instruments

    @property
    def target_manifest(self):
        from editors import TargetManifest
        return TargetManifest(
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
