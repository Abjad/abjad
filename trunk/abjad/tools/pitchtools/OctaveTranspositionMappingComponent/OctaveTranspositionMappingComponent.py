from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.pitchtools.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.NumberedChromaticPitch import NumberedChromaticPitch
from abjad.tools.pitchtools.PitchRange import PitchRange


class OctaveTranspositionMappingComponent(AbjadObject):
    '''.. versionadded:: 2.8

    Octave transposition mapping component::

        >>> pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', 15)
        OctaveTranspositionMappingComponent('[A0, C8]', 15)

    Initialize from input parameters separately, from a pair, from 
    a string or from another mapping component.

    Model ``pitchtools.transpose_chromatic_pitch_number_by_octave_transposition_mapping`` 
    input part. (See the docs for that function.)

    Octave transposition mapping components are mutable.
    '''

    ### CLASS ATTRIBUTES ###

    _default_mandatory_input_arguments = (
        repr('[A0, C8]'),
        15,
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], tuple):
            source_pitch_range, target_octave_start_pitch = args[0]
        elif len(args) == 1 and isinstance(args[0], str):
            assert ' => ' in args[0]
            source_pitch_range, target_octave_start_pitch = args[0].split(' => ')
            try:
                target_octave_start_pitch = eval(target_octave_start_pitch)
            except NameError:
                target_octave_start_pitch = NamedChromaticPitch(target_octave_start_pitch)
                target_octave_start_pitch = target_octave_start_pitch.chromatic_pitch_number
        elif len(args) == 1 and isinstance(args[0], type(self)):
            source_pitch_range = args[0].source_pitch_range
            target_octave_start_pitch = args[0].target_octave_start_pitch
        elif len(args) == 2:
            source_pitch_range, target_octave_start_pitch = args
        else:
            raise ValueError(repr(args))
        self.source_pitch_range = source_pitch_range
        self.target_octave_start_pitch = target_octave_start_pitch

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.source_pitch_range == other.source_pitch_range:
                if self.target_octave_start_pitch == other.target_octave_start_pitch:
                    return True
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '{}{}'.format(self._class_name, self._input_argument_token)

    ### PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return ()
        
    @property
    def _input_argument_token(self):
        return '({!r}, {})'.format(
            self.source_pitch_range.one_line_named_chromatic_pitch_repr, 
            self.target_octave_start_pitch)
    
    @property
    def _mandatory_argument_values(self):
        result = []
        result.append(self.source_pitch_range)
        result.append(self.target_octave_start_pitch)
        return tuple(result)

    @property
    def _one_line_menuing_summary(self):
        return '{} => {}'.format(
            self.source_pitch_range.one_line_named_chromatic_pitch_repr, self.target_octave_start_pitch)

    ### READ / WRITE ATTRIBUTES ###

    @apply
    def source_pitch_range():
        def fget(self):
            '''Read / write source pitch range::

                >>> mapping_component = pitchtools.OctaveTranspositionMappingComponent(
                ...     '[A0, C8]', 15)
                >>> mapping_component.source_pitch_range
                PitchRange('[A0, C8]')

            Return pitch range or none.
            '''
            return self._source_pitch_range
        def fset(self, source_pitch_range):
            self._source_pitch_range = PitchRange(source_pitch_range)
        return property(**locals())

    @apply
    def target_octave_start_pitch():
        def fget(self):
            '''Read / write target octave start pitch::

                >>> mapping_component = pitchtools.OctaveTranspositionMappingComponent(
                ...     '[A0, C8]', 15)
                >>> mapping_component.target_octave_start_pitch
                NumberedChromaticPitch(15)

            Return numbered chromatic pitch or none.
            '''
            return self._target_octave_start_pitch
        def fset(self, target_octave_start_pitch):
            self._target_octave_start_pitch = NumberedChromaticPitch(target_octave_start_pitch)
        return property(**locals())
