# -*- coding: utf-8 -*-
import copy
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class RegistrationComponent(AbjadValueObject):
    '''Registration component.

    ::

        >>> import abjad

    ..  container:: example

        Initializes a registration component that specifies that all pitches
        from A0 up to and including C8 should be transposed to the octave
        starting at Eb5 (numbered pitch 15):

        ::

            >>> component = abjad.RegistrationComponent('[A0, C8]', 15)
            >>> component
            RegistrationComponent(source_pitch_range=PitchRange('[A0, C8]'), target_octave_start_pitch=NumberedPitch(15))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_source_pitch_range',
        '_target_octave_start_pitch',
        )

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

    def __eq__(self, argument):
        r'''Is true when `argument` is a registration component
        with source pitch range and target octave start pitch equal to those of
        this registration component. Otherwise false.

        Returns true or false.
        '''
        return super(RegistrationComponent, self).__eq__(argument)

    def __format__(self, format_specification=''):
        r'''Formats registration component.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __hash__(self):
        r'''Hashes registration component.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(RegistrationComponent, self).__hash__()

    ### PUBLIC PROPERTIES ###

    @property
    def source_pitch_range(self):
        r'''Gets source pitch range of registration component.

        ..  container:: example

            Gets source pitch range of example component:

            ::

                >>> component.source_pitch_range
                PitchRange('[A0, C8]')

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
