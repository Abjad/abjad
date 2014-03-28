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
        self._item_class = instrumenttools.Instrument
        self._item_creator_class = wizards.InstrumentCreationWizard
        self._item_creator_class_kwargs = {'is_ranged': True}
        self._item_editor_class = editors.InstrumentEditor
        self._item_identifier = 'instrument'


    ### PUBLIC PROPERTIES ###

    @property
    def _items(self):
        return self.target.instruments

    @property
    def _target_manifest(self):
        from scoremanager.editors import TargetManifest
        return TargetManifest(
            instrumenttools.Performer,
            ('name', 'nm', getters.get_string),
            target_attribute_name='name',
            )

    ### PUBLIC METHODS ###

    def _initialize_target(self):
        if self.target is not None:
            return
        else:
            self._target = self._target_class()