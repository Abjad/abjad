# -*- encoding: utf-8 -*-
import copy
from abjad.tools.abctools.AbjadObject import AbjadObject


class RegistrationComponent(AbjadObject):
    '''Registration component.

    ..  container:: example

        **Example.** Initializes a registration component that specifies that
        all pitches from A0 up to and including C8 should be tranposed to
        the octave starting at Eb5 (numbered pitch 15):

        ::

            >>> component = pitchtools.RegistrationComponent('[A0, C8]', 15)
            >>> component
            RegistrationComponent(source_pitch_range=PitchRange(range_string='[A0, C8]'), target_octave_start_pitch=NumberedPitch(15))

    Models
    ``pitchtools.transpose_pitch_number_by_octave_transposition_mapping``
    input part. (See the docs for that function.)

    Registration components are immutable.
    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        source_pitch_range='[A0, C8]', 
        target_octave_start_pitch=0,
        ):
        from abjad.tools import pitchtools
        if isinstance(source_pitch_range, pitchtools.PitchRange):
            source_pitch_range = copy.copy(source_pitch_range)
        else:
            source_pitch_range = pitchtools.PitchRange(source_pitch_range)
        target_octave_start_pitch = pitchtools.NumberedPitch(
            target_octave_start_pitch)
        self._source_pitch_range = source_pitch_range
        self._target_octave_start_pitch = target_octave_start_pitch

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a registration component
        with source pitch range and target octave start pitch equal to those of
        this registration component. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if self.source_pitch_range == expr.source_pitch_range:
                if (self.target_octave_start_pitch ==
                    expr.target_octave_start_pitch):
                    return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats registration component.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __hash__(self):
        r'''Hashes registration component.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(RegistrationComponent, self).__hash__()

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from ide import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='source_pitch_range',
                command='pr',
                editor=idetools.getters.get_pitch_range_string,
                is_keyword=False,
                ),
            systemtools.AttributeDetail(
                name='target_octave_start_pitch',
                command='sp',
                editor=idetools.getters.get_integer,
                is_keyword=False,
                ),
            )

    @property
    def _input_argument_token(self):
        return '({!r}, {:d})'.format(
            self.source_pitch_range.one_line_named_pitch_repr,
            self.target_octave_start_pitch,
            )

    @property
    def _list_format(self):
        return (
            (
            self.source_pitch_range.start_pitch.pitch_number,
            self.source_pitch_range.stop_pitch.pitch_number
            ),
            self.target_octave_start_pitch.pitch_number
            )

    @property
    def _one_line_menu_summary(self):
        return '{} => {:d}'.format(
            self.source_pitch_range.one_line_named_pitch_repr,
            self.target_octave_start_pitch,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def source_pitch_range(self):
        r'''Gets source pitch range of registration component.

        ..  container:: example

            Gets source pitch range of example component:

            ::

                >>> component.source_pitch_range
                PitchRange(range_string='[A0, C8]')

        Returns pitch range or none.
        '''
        return self._source_pitch_range

    @property
    def target_octave_start_pitch(self):
        r'''Gets target octave start pitch of registration component.

        ..  container:: example

            Gets target octave start pitch of example component:

            ::

                >>> component.target_octave_start_pitch
                NumberedPitch(15)

        Returns numbered pitch or none.
        '''
        return self._target_octave_start_pitch