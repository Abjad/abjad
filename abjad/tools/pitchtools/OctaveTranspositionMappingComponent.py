# -*- encoding: utf-8 -*-
import copy
from abjad.tools.abctools.AbjadObject import AbjadObject


class OctaveTranspositionMappingComponent(AbjadObject):
    '''An octave transposition mapping component.

    ::

        >>> mc = pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', 15)
        >>> mc
        OctaveTranspositionMappingComponent(source_pitch_range=PitchRange(range_string='[A0, C8]'), target_octave_start_pitch=NumberedPitch(15))

    Initializes from input parameters separately, from a pair, from
    a string or from another mapping component.

    Models
    ``pitchtools.transpose_pitch_number_by_octave_transposition_mapping``
    input part. (See the docs for that function.)

    Octave transposition mapping components are mutable.

    .. todo:: make components immutable.
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
        self.source_pitch_range = source_pitch_range
        self.target_octave_start_pitch = target_octave_start_pitch

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a an octave transposition mapping component
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

    def __hash__(self):
        r'''Hashes octave transposition mapping component.

        Required to be explicitely re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(OctaveTranspositionMappingComponent, self).__hash__()

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
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
        return ((
            self.source_pitch_range.start_pitch.pitch_number,
            self.source_pitch_range.stop_pitch.pitch_number),
            self.target_octave_start_pitch.pitch_number)

    @property
    def _one_line_menu_summary(self):
        return '{} => {:d}'.format(
            self.source_pitch_range.one_line_named_pitch_repr,
            self.target_octave_start_pitch,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def source_pitch_range(self):
        r'''Gets and sets source pitch range of mapping component.

        ::

            >>> mc.source_pitch_range
            PitchRange(range_string='[A0, C8]')

        Returns pitch range or none.
        '''
        return self._source_pitch_range

    @source_pitch_range.setter
    def source_pitch_range(self, source_pitch_range):
        from abjad.tools import pitchtools
        if isinstance(source_pitch_range, str):
            source_pitch_range = pitchtools.PitchRange(source_pitch_range)
        elif isinstance(source_pitch_range, pitchtools.PitchRange):
            source_pitch_range = copy.copy(source_pitch_range)
        self._source_pitch_range = source_pitch_range

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
        from abjad.tools import pitchtools
        self._target_octave_start_pitch = pitchtools.NumberedPitch(
            target_octave_start_pitch)