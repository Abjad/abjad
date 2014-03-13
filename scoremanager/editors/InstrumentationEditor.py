# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from scoremanager import getters
from scoremanager import wizards
from scoremanager.editors.ListEditor import ListEditor


class InstrumentationEditor(ListEditor):
    r'''Instrumentation editor.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import editors
        superclass = super(InstrumentationEditor, self)
        superclass.__init__(session=session, target=target)
        self.item_class = instrumenttools.Performer
        self.item_creator_class = wizards.PerformerCreationWizard
        self.item_creator_class_kwargs = {'is_ranged': True}
        self.item_editor_class = editors.PerformerEditor
        self.item_identifier = 'performer'

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return self._target_name or 'instrumentation'

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self.target.performers

    @property
    def _target_manifest(self):
        from editors import TargetManifest
        return TargetManifest(
            instrumenttools.InstrumentationSpecifier,
            )

