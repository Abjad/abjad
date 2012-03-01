from abjad.tools.pitchtools.PitchRange import PitchRange


class PitchRangeInventory(list):
    r'''.. versionadded:: 2.7

    Abjad model of an ordered list of pitch ranges::

        abjad> pitchtools.PitchRangeInventory(['[C3, C6]', '[C4, C6]'])
        PitchRangeInventory([PitchRange('[C3, C6]'), PitchRange('[C4, C6]')])

    Pitch range inventories are mutable.
    '''

    def __init__(self, pitch_range_tokens=None):
        list.__init__(self)
        pitch_range_tokens = pitch_range_tokens or []
        pitch_ranges = []
        for pitch_range_token in pitch_range_tokens:
            pitch_ranges.append(PitchRange(pitch_range_token))
        self.extend(pitch_ranges)

    ### OVERLOADS ###

    def __contains__(self, pitch_range_token):
        pitch_range = PitchRange(pitch_range_token)
        return list.__contains__(self, pitch_range)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, list.__repr__(self))

    ### PRIVATE ATTRIBUTES ###

    @property
    def _class_name(self):
        return type(self).__name__

    @property
    def _class_name_with_tools_package(self):
        return '{}.{}'.format(self._tools_package, self._class_name)

    @property
    def _contents_repr_with_tools_package(self):
        part_reprs = []
        for element in self:
            part_repr = getattr(element, '_repr_with_tools_package', repr(element))
            part_reprs.append(part_repr)
        return ', '.join(part_reprs)

    @property
    def _repr_with_tools_package(self):
        return '{}([{}])'.format(
            self._class_name_with_tools_package, self._contents_repr_with_tools_package)

    @property
    def _tools_package(self):
        for part in reversed(self.__module__.split('.')):
            if not part == self._class_name:
                return part

    ### PUBLIC METHODS ###

    def append(self, pitch_range_token):
        '''Change `pitch_range_token` to pitch range and append::

            abjad> pitch_range_inventory = pitchtools.PitchRangeInventory(['[A0, C8]'])  
            abjad> pitch_range_inventory.append('[C3, F#5]')

        ::

            abjad> pitch_range_inventory
            PitchRangeInventory([PitchRange('[A0, C8]'), PitchRange('[C3, F#5]')])

        Return none.
        '''
        pitch_range = PitchRange(pitch_range_token)
        list.append(self, pitch_range)

    def extend(self, pitch_range_tokens):
        '''Change `pitch_range_tokens` to pitch ranges and extend::

            abjad> pitch_range_inventory = pitchtools.PitchRangeInventory(['[A0, C8]'])  
            abjad> pitch_range_inventory.extend(['[C3, F#5]', '[C#4, C#5]'])

        ::

            abjad> pitch_range_inventory
            PitchRangeInventory([PitchRange('[A0, C8]'), PitchRange('[C3, F#5]'), PitchRange('[C#4, C#5]')])

        Return none.
        '''
        pitch_ranges = []
        for pitch_range_token in pitch_range_tokens:
            pitch_ranges.append(PitchRange(pitch_range_token))
        list.extend(self, pitch_ranges)
