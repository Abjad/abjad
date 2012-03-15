from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from abjad.tools.pitchtools.OctaveTranspositionMappingComponent import OctaveTranspositionMappingComponent


class OctaveTranspositionMapping(ObjectInventory):
    '''.. versionadded:: 2.8

    Octave transposition mapping::

        abjad> pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
        OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])

    Octave transposition mappings model 
    ``pitchtools.transpose_chromatic_pitch_number_by_octave_transposition_mapping`` input.

    Octave transposition mappings implement the list interface and are mutable.
    '''

    ### SPECIAL METHODS ###

    def __repr__(self):
        if self.inventory_name:
            return '{}([{}], inventory_name={!r})'.format(
                self._class_name, self._repr_contents_string, self.inventory_name)
        else:
            return '{}([{}])'.format(self._class_name, self._repr_contents_string)

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _item_callable(self):
        return OctaveTranspositionMappingComponent

    @property
    def _one_line_menuing_summary(self):
        name = self.inventory_name or 'mapping'
        contents = []
        for mapping_component in self:
            contents.append(mapping_component._one_line_menuing_summary)
        contents_string = ', '.join(contents)
        return '{}: {}'.format(name, contents_string)

    @property
    def _repr_contents_string(self):
        result = []
        for mapping_component in self:
            result.append(mapping_component._input_argument_token)
        return ', '.join(result)
