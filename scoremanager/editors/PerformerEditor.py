# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from scoremanager import getters
from scoremanager import wizards
from scoremanager.editors.ListEditor import ListEditor


class PerformerEditor(ListEditor):
    r'''Performer editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        superclass = super(PerformerEditor, self)
        superclass.__init__(session=session, target=target)
        self._item_class = instrumenttools.Instrument
        self._item_creator_class = wizards.InstrumentCreationWizard
        self._item_creator_class_kwargs = {'is_ranged': True}
        self._item_identifier = 'instrument'

    ### PUBLIC PROPERTIES ###

    @property
    def _items(self):
        return self.target.instruments

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        return systemtools.AttributeManifest(
            instrumenttools.Performer,
            systemtools.AttributeDetail(
                name='name', 
                menu_key='nm', 
                editor_callable=getters.get_string,
                ),
            )

    ### PUBLIC METHODS ###

    def _initialize_target(self):
        if self.target is not None:
            return
        else:
            self._target = self._target_class()