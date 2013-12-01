# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.pitchtools.NamedPitch import NamedPitch
from abjad.tools.pitchtools.NumberedPitch import NumberedPitch
from abjad.tools.pitchtools.PitchRange import PitchRange


class OctaveTranspositionMappingComponent(AbjadObject):
    '''An octave transposition mapping component.

    ::

        >>> mc = pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', 15)
        >>> mc
        OctaveTranspositionMappingComponent('[A0, C8]', 15)

    Initializes from input parameters separately, from a pair, from
    a string or from another mapping component.

    Models
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
        r'''True when `expr` is a an octave transposition mapping component
        with source pitch range and target octave start pitch equal to those of
        this octave transposition mapping component. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if self.source_pitch_range == expr.source_pitch_range:
                if self.target_octave_start_pitch == \
                    expr.target_octave_start_pitch:
                    return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats mapping component.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __ne__(self, expr):
        r'''True when octave transposition mapping component does not equal 
        `expr`. Otherwise false.

        Returns boolean.
        '''
        return not self == expr

    ### PRIVATE PROPERTIES ###

    @property
    def _input_argument_token(self):
        return '({!r}, {:d})'.format(
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
        return '{} => {:d}'.format(
            self.source_pitch_range.one_line_named_pitch_repr,
            self.target_octave_start_pitch,
            )

    @property
    def _repr_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            positional_argument_values=(
                self.source_pitch_range.one_line_named_pitch_repr,
                self.target_octave_start_pitch.pitch_number,
                ),
            )

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=(
                self.source_pitch_range,
                self.target_octave_start_pitch,
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def source_pitch_range(self):
        r'''Gets and sets source pitch range of mapping component.

        ::

            >>> mc.source_pitch_range
            PitchRange('[A0, C8]')

        Returns pitch range or none.
        '''
        return self._source_pitch_range

    @source_pitch_range.setter
    def source_pitch_range(self, source_pitch_range):
        self._source_pitch_range = PitchRange(source_pitch_range)

    @property
    def target_octave_start_pitch(self):
        r'''Gets and sets target octave start pitch of mapping component.

        ::

            >>> mc.target_octave_start_pitch
            NumberedPitch(15)

        Returns numbered pitch or none.
        '''
        return self._target_octave_start_pitch

    @target_octave_start_pitch.setter
    def target_octave_start_pitch(self, target_octave_start_pitch):
        self._target_octave_start_pitch = NumberedPitch(
            target_octave_start_pitch)
