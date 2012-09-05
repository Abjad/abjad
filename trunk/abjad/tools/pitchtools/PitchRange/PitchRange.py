import numbers
from abjad.tools.abctools import AbjadObject


class PitchRange(AbjadObject):
    r""".. versionadded:: 2.0

    Abjad model of pitch range::

        >>> pitchtools.PitchRange(-12, 36)
        PitchRange('[C3, C7]')

    Initalize from pitch numbers, pitch names, pitch instances, one-line reprs 
    or other pitch range objects.

    Pitch ranges test for equality and inequality against other pitch ranges.

    Pitch ranges test less than, greater than, less-equal and greater-equal against pitches.
    
    Pitch ranges do not sort relative to other pitch ranges.

    Pitch ranges are immutable.
    """

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_start', '_stop', '_pitch_range_name', '_pitch_range_name_markup', )

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from abjad.tools import pitchtools
        if len(args) == 1 and isinstance(args[0], type(self)):
            if args[0].start_pitch_is_included_in_range:
                indicator = 'inclusive'
            else:
                indicator = 'exclusive'
            start = (args[0].start_pitch, indicator)
            object.__setattr__(self, '_start', start)
            assert isinstance(args[0], type(self))
            if args[0].stop_pitch_is_included_in_range:
                indicator = 'inclusive'
            else:
                indicator = 'exclusive'
            stop = (args[0].stop_pitch, indicator)
            object.__setattr__(self, '_stop', stop)
        elif len(args) == 1 and isinstance(args[0], str):
            self._init_by_symbolic_pitch_range_string(*args)
        elif len(args) == 1 and isinstance(args[0], (tuple, list)):
            start, stop = args[0]
            type(self).__init__(self, start, stop)
        else:
            assert len(args) == 2
            start, stop = args
            if start is None:
                start = start
            elif isinstance(start, (int, long, float, str)):
                pitch = pitchtools.NamedChromaticPitch(start)
                start = (pitch, 'inclusive')
            else:
                assert len(start) == 2
                pitch, containment = start
                assert containment in ('inclusive', 'exclusive')
                pitch = pitchtools.NamedChromaticPitch(pitch)
                start = (pitch, containment)
            object.__setattr__(self, '_start', start)
            if stop is None:
                stop = stop
            elif isinstance(stop, (int, long, float, str)):
                pitch = pitchtools.NamedChromaticPitch(stop)
                stop = (pitch, 'inclusive')
            else:
                assert len(stop) == 2
                pitch, containment = stop
                assert containment in ('inclusive', 'exclusive')
                pitch = pitchtools.NamedChromaticPitch(pitch)
                stop = (pitch, containment)
            object.__setattr__(self, '_stop', stop)
        pitch_range_name = kwargs.get('pitch_range_name')
        object.__setattr__(self, '_pitch_range_name', pitch_range_name)
        pitch_range_name_markup = kwargs.get('pitch_range_name_markup')
        object.__setattr__(self, '_pitch_range_name_markup', pitch_range_name_markup)

    ### SPECIAL METHODS ###

    def __contains__(self, arg):
        from abjad.tools import containertools
        from abjad.tools import pitchtools
        from abjad.tools import resttools
        from abjad.tools import skiptools
        from abjad.tools.chordtools.Chord import Chord
        from abjad.tools.notetools.Note import Note
        if getattr(arg, 'written_pitch_indication_is_nonsemantic', False):
            return True
        elif isinstance(arg, (int, long, float)):
            pitch = pitchtools.NamedChromaticPitch(arg)
            return self._contains_pitch(pitch)
        elif isinstance(arg, pitchtools.NamedChromaticPitch):
            return self._contains_pitch(arg)
        elif isinstance(arg, Note):
            return self._contains_pitch(arg.sounding_pitch)
        elif isinstance(arg, Chord):
            return all([self._contains_pitch(x) for x in arg.sounding_pitches])
        elif isinstance(arg, (resttools.Rest, skiptools.Skip)):
            return True
        elif isinstance(arg, containertools.Container):
            return all([x in self for x in arg.leaves])
        else:
            pitches = pitchtools.list_named_chromatic_pitches_in_expr(arg)
            if pitches:
                return all([self._contains_pitch(x) for x in pitches])
            else:
                try:
                    return all([self._contains_pitch(x) for x in arg])
                except TypeError:
                    return False
        return False

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self._start == arg._start:
                if self._stop == arg._stop:
                    return True
        return False

    def __ge__(self, arg):
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedChromaticPitch(arg)
            if self.start_pitch is None:
                return False
            return pitch <= self.start_pitch
        except (TypeError, ValueError):
            return False

    def __gt__(self, arg):
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedChromaticPitch(arg)
            if self.start_pitch is None:
                return False
            return pitch < self.start_pitch
        except (TypeError, ValueError):
            return False

    def __le__(self, arg):
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedChromaticPitch(arg)
            if self.stop_pitch is None:
                return False
            return self.stop_pitch <= pitch
        except (TypeError, ValueError):
            return False

    def __lt__(self, arg):
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedChromaticPitch(arg)
            if self.stop_pitch is None:
                return False
            return self.stop_pitch < pitch
        except (TypeError, ValueError):
            return False

    def __ne__(self, arg):
        return not self == arg

    ### PRIVATE CLASS ATTRIBUTES ###

    _start_punctuation_to_inclusivity_string = {
        '[': 'inclusive',
        '(': 'exclusive'}

    _stop_punctuation_to_inclusivity_string = {
        ']': 'inclusive',
        ')': 'exclusive'}

    ### PRIVATE PROPERTIES ###

    @property
    def _close_bracket_string(self):
        if self.stop_pitch_is_included_in_range:
            return ']'
        else:
            return ')'

    @property
    def _keyword_argument_names(self):
        result = []
        result.append('pitch_range_name')
        result.append('pitch_range_name_markup')
        return tuple(result)

    @property
    def _mandatory_argument_values(self):
        result = []
        result.append(self.one_line_named_chromatic_pitch_repr)
        return tuple(result)

    @property
    def _one_line_menuing_summary(self):
        return self.one_line_named_chromatic_pitch_repr

    @property
    def _open_bracket_string(self):
        if self.start_pitch_is_included_in_range:
            return '['
        else:
            return '('

    ### PRIVATE METHODS ###

    def _contains_pitch(self, pitch):
        from abjad.tools import pitchtools
        if isinstance(pitch, numbers.Number):
            pitch = pitchtools.NamedChromaticPitch(pitch)
        elif isinstance(pitch, str):
            pitch = pitchtools.NamedChromaticPitch(pitch)
        if self._start is None and self._stop is None:
            return True
        elif self._start is None:
            if self.stop_pitch_is_included_in_range:
                return pitch <= self.stop_pitch
            else:
                return pitch < self.stop_pitch
        elif self._stop is None:
            if self.start_pitch_is_included_in_range:
                return self.start_pitch <= pitch
            else:
                return self.start_pitch < pitch
        else:
            if self.start_pitch_is_included_in_range:
                if self.stop_pitch_is_included_in_range:
                    return self.start_pitch <= pitch <= self.stop_pitch
                else:
                    return self.start_pitch <= pitch < self.stop_pitch
            else:
                if self.stop_pitch_is_included_in_range:
                    return self.start_pitch < pitch <= self.stop_pitch
                else:
                    return self.start_pitch < pitch < self.stop_pitch

    def _init_by_symbolic_pitch_range_string(self, symbolic_pitch_range_string):
        from abjad.tools import pitchtools
        from abjad.tools.pitchtools.is_symbolic_pitch_range_string import symbolic_pitch_range_string_regex
        assert pitchtools.is_symbolic_pitch_range_string(symbolic_pitch_range_string)
        groups = symbolic_pitch_range_string_regex.match(symbolic_pitch_range_string).groups()
        start_punctuation = groups[0]
        start_pitch_string = groups[1]
        stop_pitch_string = groups[8]
        stop_punctuation = groups[-1]
        start_inclusivity_string = self._start_punctuation_to_inclusivity_string[start_punctuation]
        stop_inclusivity_string = self._stop_punctuation_to_inclusivity_string[stop_punctuation]
        start_pair = (start_pitch_string, start_inclusivity_string)
        stop_pair = (stop_pitch_string, stop_inclusivity_string)
        type(self).__init__(self, start_pair, stop_pair)

    
    ### PUBLIC PROPERTIES ###

    @property
    def one_line_named_chromatic_pitch_repr(self):
        r'''Read-only one-line named chromatic pitch repr of pitch of range::

            >>> pitch_range = pitchtools.PitchRange(-12, 36)
            >>> pitch_range.one_line_named_chromatic_pitch_repr
            '[C3, C7]'

        Return string.
        '''
        result = []
        result.append(self._open_bracket_string)
        if self.start_pitch:
            result.append(self.start_pitch.pitch_class_octave_label)
            result.append(', ')
        if self.stop_pitch:
            result.append(self.stop_pitch.pitch_class_octave_label)
        result.append(self._close_bracket_string)
        result = ''.join(result)
        return result

    @property
    def one_line_numbered_chromatic_pitch_repr(self):
        r'''Read-only one-line numbered chromatic pitch repr of pitch of range::

            >>> pitch_range = pitchtools.PitchRange(-12, 36)
            >>> pitch_range.one_line_numbered_chromatic_pitch_repr
            '[-12, 36]'

        Return string.
        '''
        result = []
        result.append(self._open_bracket_string)
        result.append(str(self.start_pitch.numbered_chromatic_pitch))
        result.append(', ')
        result.append(str(self.stop_pitch.numbered_chromatic_pitch))
        result.append(self._close_bracket_string)
        result = ''.join(result)
        return result

    @property
    def pitch_range_name(self):
        r'''.. versionadded:: 2.7

        Read-only name of pitch range::

            >>> pitch_range = pitchtools.PitchRange(-12, 36, pitch_range_name='four-octave range')
            >>> pitch_range.pitch_range_name
            'four-octave range'

        Return string or none.
        '''
        return self._pitch_range_name

    @property
    def pitch_range_name_markup(self):
        r'''.. versionadded:: 2.7

        Read-only markup of pitch range name::

            >>> from abjad.tools.markuptools import Markup

        ::

            >>> pitch_range = pitchtools.PitchRange(-12, 36, 
            ...     pitch_range_name_markup=Markup('four-octave range'))
            >>> pitch_range.pitch_range_name_markup
            Markup(('four-octave range',))

        Default to `pitch_range_name` when `pitch_range_name_markup` not set explicitly.

        Return markup or none.
        '''
        from abjad.tools import markuptools
        if self._pitch_range_name_markup:
            return self._pitch_range_name_markup
        elif self.pitch_range_name:
            return markuptools.Markup(self.pitch_range_name)

    @property
    def start_pitch(self):
        r'''Read-only start pitch of range::

            >>> pitch_range = pitchtools.PitchRange(-12, 36)
            >>> pitch_range.start_pitch
            NamedChromaticPitch('c')

        Return pitch.
        '''
        if self._start is None:
            return None
        return self._start[0]

    @property
    def start_pitch_is_included_in_range(self):
        '''Read-only boolean true when start pitch is included in range. Otherwise false::

            >>> pitch_range = pitchtools.PitchRange(-12, 36)
            >>> pitch_range.start_pitch_is_included_in_range
            True

        Return boolean.
        '''
        if self._start is None:
            return True
        return self._start[1] == 'inclusive'

    @property
    def stop_pitch(self):
        r"""Read-only stop pitch of range::

            >>> pitch_range = pitchtools.PitchRange(-12, 36)
            >>> pitch_range.stop_pitch
            NamedChromaticPitch("c''''")

        Return pitch.
        """
        if self._stop is None:
            return None
        return self._stop[0]

    @property
    def stop_pitch_is_included_in_range(self):
        '''Read-only boolean true when stop pitch is included in range. Otherwise false::

            >>> pitch_range = pitchtools.PitchRange(-12, 36)
            >>> pitch_range.stop_pitch_is_included_in_range
            True

        Return boolean.
        '''
        if self._stop is None:
            return True
        return self._stop[1] == 'inclusive'
