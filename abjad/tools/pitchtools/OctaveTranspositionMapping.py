# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList
from abjad.tools.pitchtools.OctaveTranspositionMappingComponent \
    import OctaveTranspositionMappingComponent


class OctaveTranspositionMapping(TypedList):
    '''An octave transposition mapping.

    ::

        >>> mapping = pitchtools.OctaveTranspositionMapping(
        ...     [('[A0, C4)', 15), ('[C4, C8)', 27)])

    ::

        >>> mapping
        OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])

    Octave transposition mappings model
    ``pitchtools.transpose_pitch_number_by_octave_transposition_mapping``
    input.

    Octave transposition mappings implement the list interface and
    are mutable.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, pitches):
        r'''Call octave transposition mapping on `pitches`.

            >>> mapping([-24, -22, -23, -21])
            [24, 26, 25, 15]

        ::

            >>> mapping([0, 2, 1, 3])
            [36, 38, 37, 27]

        Returns list.
        '''
        transposed_pitches = [self._transpose_pitch(x) for x in pitches]
        return transposed_pitches

    def __format__(self, format_specification=''):
        r'''Formats octave transposition mapping.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ::

            >>> print format(mapping)
            pitchtools.OctaveTranspositionMapping(
                [
                    pitchtools.OctaveTranspositionMappingComponent(
                        pitchtools.PitchRange(
                            '[A0, C4)'
                            ),
                        pitchtools.NumberedPitch(15)
                        ),
                    pitchtools.OctaveTranspositionMappingComponent(
                        pitchtools.PitchRange(
                            '[C4, C8)'
                            ),
                        pitchtools.NumberedPitch(27)
                        ),
                    ]
                )

        Returns string.
        '''
        superclass = super(OctaveTranspositionMapping, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _transpose_pitch(self, pitch):
        from abjad.tools import pitchtools
        pitch = pitchtools.NamedPitch(pitch)
        target_pitch_class_number = pitch.pitch_class_number
        for component in self:
            if pitch in component.source_pitch_range:
                target_octave = range(
                    component.target_octave_start_pitch.pitch_number,
                    component.target_octave_start_pitch.pitch_number
                    + 12)
                for candidate_pitch in target_octave:
                    if candidate_pitch % 12 == \
                        pitch.pitch_class_number:
                        return candidate_pitch
        return pitch

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return OctaveTranspositionMappingComponent

    @property
    def _one_line_menuing_summary(self):
        name = self.custom_identifier or 'mapping'
        contents = []
        for mapping_component in self:
            contents.append(mapping_component._one_line_menuing_summary)
        contents_string = ', '.join(contents)
        return '{}: {}'.format(name, contents_string)

    @property
    def _repr_specification(self):
        from abjad.tools import systemtools
        input_argument_tokens = []
        for mapping_component in self:
            token = (
                mapping_component.source_pitch_range.one_line_named_pitch_repr,
                mapping_component.target_octave_start_pitch.pitch_number
                )
            input_argument_tokens.append(token)
        keyword_argument_names = []
        if self.custom_identifier is not None:
            keyword_argument_names.append('custom_identifier')
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=(
                input_argument_tokens,
                ),
            )
