# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.pitchtools.NamedPitch import NamedPitch
from abjad.tools.pitchtools.NumberedPitch \
	import NumberedPitch
from abjad.tools.pitchtools.PitchRange import PitchRange


class OctaveTranspositionMappingComponent(AbjadObject):
    '''An octave transposition mapping component.

    ::

        >>> mc = pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', 15)
        >>> mc
        OctaveTranspositionMappingComponent('[A0, C8]', 15)

    Initialize from input parameters separately, from a pair, from
    a string or from another mapping component.

    Model 
    ``pitchtools.transpose_pitch_number_by_octave_transposition_mapping``
    input part. (See the docs for that function.)

    Octave transposition mapping components are mutable.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        repr('[A0, C8]'),
        15,
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], tuple):
            source_pitch_range, target_octave_start_pitch = args[0]
        elif len(args) == 1 and isinstance(args[0], str):
            assert ' => ' in args[0]
            source_pitch_range, target_octave_start_pitch = \
                args[0].split(' => ')
            try:
                target_octave_start_pitch = eval(target_octave_start_pitch)
            except NameError:
                target_octave_start_pitch = NamedPitch(
                    target_octave_start_pitch)
                target_octave_start_pitch = \
                    target_octave_start_pitch.pitch_number
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

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.source_pitch_range == expr.source_pitch_range:
                if self.target_octave_start_pitch == \
                    expr.target_octave_start_pitch:
                    return True
        return False

    def __ne__(self, expr):
        return not self == expr

    def __repr__(self):
        return '{}{}'.format(self._class_name, self._input_argument_token)

    ### PRIVATE PROPERTIES ###

    @property
    def _input_argument_token(self):
        return '({!r}, {})'.format(
            self.source_pitch_range.one_line_named_pitch_repr,
            self.target_octave_start_pitch)

    @property
    def _keyword_argument_names(self):
        return ()

    @property
    def _list_format(self):
        return ((
            self.source_pitch_range.start_pitch.pitch_number,
            self.source_pitch_range.stop_pitch.pitch_number),
            self.target_octave_start_pitch.pitch_number)

    @property
    def _one_line_menuing_summary(self):
        return '{} => {}'.format(
            self.source_pitch_range.one_line_named_pitch_repr, 
            self.target_octave_start_pitch,
            )

    @property
    def _positional_argument_values(self):
        result = []
        result.append(self.source_pitch_range)
        result.append(self.target_octave_start_pitch)
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @apply
    def source_pitch_range():
        def fget(self):
            r'''Read / write source pitch range:

            ::

                >>> mc.source_pitch_range
                PitchRange('[A0, C8]')

            Returns pitch range or none.
            '''
            return self._source_pitch_range
        def fset(self, source_pitch_range):
            self._source_pitch_range = PitchRange(source_pitch_range)
        return property(**locals())

    @apply
    def target_octave_start_pitch():
        def fget(self):
            r'''Read / write target octave start pitch:

            ::

                >>> mc.target_octave_start_pitch
                NumberedPitch(15)

            Returns numbered pitch or none.
            '''
            return self._target_octave_start_pitch
        def fset(self, target_octave_start_pitch):
            self._target_octave_start_pitch = NumberedPitch(
                target_octave_start_pitch)
        return property(**locals())
