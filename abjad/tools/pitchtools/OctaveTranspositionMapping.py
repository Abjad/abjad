# -*- encoding: utf-8 -*-
import copy
from abjad.tools.datastructuretools.TypedList import TypedList


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

    ### CLASS VARIABLES ###

    __slots__ = (
        )

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

            >>> print(format(mapping))
            pitchtools.OctaveTranspositionMapping(
                [
                    pitchtools.OctaveTranspositionMappingComponent(
                        source_pitch_range=pitchtools.PitchRange(
                            range_string='[A0, C4)',
                            ),
                        target_octave_start_pitch=pitchtools.NumberedPitch(15),
                        ),
                    pitchtools.OctaveTranspositionMappingComponent(
                        source_pitch_range=pitchtools.PitchRange(
                            range_string='[C4, C8)',
                            ),
                        target_octave_start_pitch=pitchtools.NumberedPitch(27),
                        ),
                    ]
                )

        Returns string.
        '''
        superclass = super(OctaveTranspositionMapping, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        return systemtools.AttributeManifest()

    @staticmethod
    def _item_callable(expr):
        from abjad.tools import pitchtools
        if isinstance(expr, tuple):
            component = pitchtools.OctaveTranspositionMappingComponent(*expr)
        elif isinstance(expr, pitchtools.OctaveTranspositionMappingComponent):
            component = copy.copy(expr)
        else:
            raise TypeError(repr(expr))
        return component

    @property
    def _one_line_menu_summary(self):
        name = 'mapping'
        contents = []
        for mapping_component in self:
            contents.append(mapping_component._one_line_menu_summary)
        contents_string = ', '.join(contents)
        return '{}: {}'.format(name, contents_string)

    @property
    def _repr_specification(self):
        from abjad.tools import systemtools
        input_argument_tokens = []
        for mapping_component in self:
            item = (
                mapping_component.source_pitch_range.one_line_named_pitch_repr,
                mapping_component.target_octave_start_pitch.pitch_number
                )
            input_argument_tokens.append(item)
        keyword_argument_names = []
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=(
                input_argument_tokens,
                ),
            )

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