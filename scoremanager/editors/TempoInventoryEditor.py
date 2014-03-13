# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from scoremanager import getters
from scoremanager.editors.ObjectInventoryEditor import ObjectInventoryEditor


class TempoInventoryEditor(ObjectInventoryEditor):
    r'''TempoInventory editor.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import editors
        from scoremanager import iotools
        superclass = super(TempoInventoryEditor, self)
        superclass.__init__(session=session, target=target)
        self.item_class = indicatortools.Tempo
        self.item_editor_class = editors.TempoEditor
        self.item_getter_configuration_method = \
            iotools.UserInputGetter.append_tempo
        self.item_identifier = 'tempo'

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        from editors import TargetManifest
        return TargetManifest(
            indicatortools.TempoInventory,
            target_name_attribute='inventory name',
            )
