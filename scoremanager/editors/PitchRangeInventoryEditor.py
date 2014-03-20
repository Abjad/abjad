# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from scoremanager.editors.Editor import Editor
from scoremanager.editors.ObjectInventoryEditor import ObjectInventoryEditor


class PitchRangeInventoryEditor(ObjectInventoryEditor):
    r'''PitchRangeInventory editor.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import editors
        from scoremanager import iotools
        superclass = super(PitchRangeInventoryEditor, self)
        superclass.__init__(session=session, target=target)
        self.item_getter_configuration_method = \
            iotools.UserInputGetter.append_symbolic_pitch_range_string
        self.item_class = pitchtools.PitchRange
        self.item_editor_class = editors.PitchRangeEditor
        self.item_identifier = 'pitch range'


    ### PUBLIC PROPERTIES ###

    @property
    def _target_manifest(self):
        from scoremanager.editors import TargetManifest
        return TargetManifest(
            pitchtools.PitchRangeInventory,
            target_name_attribute='name',
            )

    @property
    def _target_summary_lines(self):
        result = []
        for pitch_range in self.target:
            result.append(repr(pitch_range))
        return result
