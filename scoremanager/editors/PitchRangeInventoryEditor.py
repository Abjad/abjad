# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from scoremanager.editors.ListEditor import ListEditor


class PitchRangeInventoryEditor(ListEditor):
    r'''PitchRangeInventory editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        from scoremanager import editors
        from scoremanager import iotools
        superclass = super(PitchRangeInventoryEditor, self)
        superclass.__init__(session=session, target=target)
        self._item_getter_configuration_method = \
            iotools.UserInputGetter.append_symbolic_pitch_range_string
        # TODO: derive from self._attribute_manifest?
        self._item_class = pitchtools.PitchRange
        # TODO: derive from self._item_class?
        self._item_identifier = 'pitch range'


    ### PUBLIC PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        return systemtools.AttributeManifest(
            pitchtools.PitchRangeInventory,
            target_name_attribute='name',
            )

    @property
    def _target_summary_lines(self):
        result = []
        for pitch_range in self.target:
            result.append(repr(pitch_range))
        return result