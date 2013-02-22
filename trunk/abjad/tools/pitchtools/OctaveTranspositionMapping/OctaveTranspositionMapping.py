from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from abjad.tools.pitchtools.OctaveTranspositionMappingComponent import OctaveTranspositionMappingComponent


class OctaveTranspositionMapping(ObjectInventory):
    '''.. versionadded:: 2.8

    Octave transposition mapping::

        >>> mapping = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])

    ::

        >>> mapping
        OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])

    Octave transposition mappings model 
    ``pitchtools.transpose_chromatic_pitch_number_by_octave_transposition_mapping`` input.

    Octave transposition mappings implement the list interface and are mutable.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, pitches):
        '''Call octave transposition mapping on `pitches`.

            >>> mapping([-24, -22, -23, -21])
            [24, 26, 25, 15]

        ::

            >>> mapping([0, 2, 1, 3])
            [36, 38, 37, 27]

        Return list.
        '''
        transposed_pitches = [self._transpose_pitch(x) for x in pitches]
        return transposed_pitches

    def _transpose_pitch(self, pitch):
        from abjad.tools import pitchtools
        pitch = pitchtools.NamedChromaticPitch(pitch)
        target_pitch_class_number = pitch.chromatic_pitch_class_number
        for component in self:
            if pitch in component.source_pitch_range:
                target_octave = range(
                    component.target_octave_start_pitch.chromatic_pitch_number, 
                    component.target_octave_start_pitch.chromatic_pitch_number + 12)
                for candidate_pitch in target_octave:
                    if candidate_pitch % 12 == pitch.chromatic_pitch_class_number:
                        return candidate_pitch
                            
    def __repr__(self):
        if self.name:
            return '{}([{}], name={!r})'.format(
                self._class_name, self._repr_contents_string, self.name)
        else:
            return '{}([{}])'.format(self._class_name, self._repr_contents_string)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return OctaveTranspositionMappingComponent

    @property
    def _one_line_menuing_summary(self):
        name = self.name or 'mapping'
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

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def storage_format(self):
        '''Octave transposition mapping storage format.

        ::

            >>> z(mapping)
            pitchtools.OctaveTranspositionMapping([
                pitchtools.OctaveTranspositionMappingComponent(
                    pitchtools.PitchRange(
                        '[A0, C4)'
                        ),
                    pitchtools.NumberedChromaticPitch(
                        15
                        )
                    ),
                pitchtools.OctaveTranspositionMappingComponent(
                    pitchtools.PitchRange(
                        '[C4, C8)'
                        ),
                    pitchtools.NumberedChromaticPitch(
                        27
                        )
                    )
                ])

        Return string.
        '''
        return ObjectInventory.storage_format.fget(self)
