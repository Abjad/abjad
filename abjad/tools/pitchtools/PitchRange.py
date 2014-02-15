# -*- encoding: utf-8 -*-
import collections
import numbers
import re
from abjad.tools import datastructuretools
from abjad.tools import indicatortools
from abjad.tools.abctools import AbjadObject
from abjad.tools.pitchtools.Pitch import Pitch
from abjad.tools.topleveltools import inspect_


# TODO: make iterable so that for x in PitchRange works
class PitchRange(AbjadObject):
    r"""A pitch range.

    ::

        >>> pitch_range = pitchtools.PitchRange(-12, 36,
        ...     pitch_range_name='four-octave range')
        >>> print format(pitch_range)
        pitchtools.PitchRange(
            '[C3, C7]',
            pitch_range_name='four-octave range',
            pitch_range_name_markup=markuptools.Markup(
                contents=('four-octave range',),
                ),
            )

    ::

        >>> show(pitch_range) # doctest: +SKIP

    Initalize from pitch numbers, pitch names, pitch instances,
    one-line reprs or other pitch range objects.

    Pitch ranges implement equality testing against other pitch ranges.

    Pitch ranges test less than, greater than, less-equal and
    greater-equal against pitches.

    Pitch ranges do not sort relative to other pitch ranges.

    Pitch ranges are immutable.
    """

    ### CLASS VARIABLES ###

    _symbolic_pitch_range_string_regex_body = '''
        ([\[(])         # open bracket or open parenthesis
        ({}|{}|-?\d+)   # pitch
        ,               # comma
        [ ]*            # any amount of whitespace
        ({}|{}|-?\d+)   # pitch
        ([\])])         # close bracket or close parenthesis
        '''.format(
            Pitch._pitch_class_octave_number_regex_body,
            Pitch._pitch_name_regex_body,
            Pitch._pitch_class_octave_number_regex_body,
            Pitch._pitch_name_regex_body,
            )

    _symbolic_pitch_range_string_regex = re.compile(
        '^{}$'.format(_symbolic_pitch_range_string_regex_body),
        re.VERBOSE,
        )

    __slots__ = (
        '_start',
        '_stop',
        '_pitch_range_name',
        '_pitch_range_name_markup',
        )

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from abjad.tools import pitchtools
        if len(args) == 1 and isinstance(args[0], type(self)):
            if args[0].start_pitch_is_included_in_range:
                boundedness = 'inclusive'
            else:
                boundedness = 'exclusive'
            start = (args[0].start_pitch, boundedness)
            self._start = start
            assert isinstance(args[0], type(self)), repr(args[0])
            if args[0].stop_pitch_is_included_in_range:
                boundedness = 'inclusive'
            else:
                boundedness = 'exclusive'
            stop = (args[0].stop_pitch, boundedness)
            self._stop = stop
        elif len(args) == 1 and isinstance(args[0], str):
            self._initialize_by_symbolic_pitch_range_string(*args)
        elif len(args) == 1 and isinstance(args[0], collections.Sequence):
            start, stop = args[0]
            type(self).__init__(self, start, stop)
        elif len(args) == 0:
            start_pitch = pitchtools.NamedPitch('A0')
            stop_pitch = pitchtools.NamedPitch('C8')
            self._start = (start_pitch, 'inclusive')
            self._stop = (stop_pitch, 'inclusive')
        else:
            assert len(args) == 2, repr(args)
            start, stop = args
            if start is None:
                start = start
            elif isinstance(start, (
                pitchtools.Pitch,
                int,
                long,
                float,
                str,
                )):
                pitch = pitchtools.NamedPitch(start)
                start = (pitch, 'inclusive')
            else:
                assert len(start) == 2, repr(start)
                pitch, containment = start
                assert containment in ('inclusive', 'exclusive')
                pitch = pitchtools.NamedPitch(pitch)
                start = (pitch, containment)
            self._start = start
            if stop is None:
                stop = stop
            elif isinstance(stop, (
                pitchtools.Pitch,
                int,
                long,
                float,
                str,
                )):
                pitch = pitchtools.NamedPitch(stop)
                stop = (pitch, 'inclusive')
            else:
                assert len(stop) == 2, repr(stop)
                pitch, containment = stop
                assert containment in ('inclusive', 'exclusive'), \
                    repr(containment)
                pitch = pitchtools.NamedPitch(pitch)
                stop = (pitch, containment)
            self._stop = stop
        pitch_range_name = kwargs.get('pitch_range_name')
        self._pitch_range_name = pitch_range_name
        pitch_range_name_markup = kwargs.get('pitch_range_name_markup')
        self._pitch_range_name_markup = pitch_range_name_markup

    ### SPECIAL METHODS ###

    def __contains__(self, arg):
        r'''Is true when pitch range contains `arg`. Otherwise false.

        Returns boolean.
        '''
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        if hasattr(arg, '_has_effective_indicator') and \
            arg._has_effective_indicator(indicatortools.IsUnpitched):
            return True
        elif isinstance(arg, (int, long, float)):
            pitch = pitchtools.NamedPitch(arg)
            return self._contains_pitch(pitch)
        elif isinstance(arg, pitchtools.NamedPitch):
            return self._contains_pitch(arg)
        elif isinstance(arg, scoretools.Note):
            sounding_pitch = inspect_(arg).get_sounding_pitch()
            return self._contains_pitch(sounding_pitch)
        elif isinstance(arg, scoretools.Chord):
            sounding_pitches = inspect_(arg).get_sounding_pitches()
            return all(self._contains_pitch(x) for x in sounding_pitches)
        elif isinstance(arg, (scoretools.Rest, scoretools.Skip)):
            return True
        elif isinstance(arg, scoretools.Container):
            return all(x in self for x in arg.select_leaves())
        else:
            pitches = pitchtools.list_named_pitches_in_expr(arg)
            if pitches:
                return all(self._contains_pitch(x) for x in pitches)
            else:
                try:
                    return all(self._contains_pitch(x) for x in arg)
                except TypeError:
                    return False
        return False

    def __eq__(self, arg):
        r'''Is true when `arg` is a pitch range with start and stop equal to those
        of this pitch range. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self._start == arg._start:
                if self._stop == arg._stop:
                    return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats pitch range.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __ge__(self, arg):
        r'''Is true when start pitch of pitch range is greater than or equal to
        `arg`. Otherwise false.

        Returns boolean.
        '''
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedPitch(arg)
            if self.start_pitch is None:
                return False
            return pitch <= self.start_pitch
        except (TypeError, ValueError):
            return False

    def __gt__(self, arg):
        r'''Is true when start pitch of pitch range is greater than `arg`.
        Otherwise false.

        Returns boolean.
        '''
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedPitch(arg)
            if self.start_pitch is None:
                return False
            return pitch < self.start_pitch
        except (TypeError, ValueError):
            return False

    def __illustrate__(self):
        r'''Illustrates pitch range.

        ::

            >>> show(pitch_range) # doctest: +SKIP

        Returns LilyPond file.
        '''
        from abjad.tools import durationtools
        from abjad.tools import lilypondfiletools
        from abjad.tools import indicatortools
        from abjad.tools import markuptools
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import attach
        from abjad.tools.topleveltools import iterate
        from abjad.tools.topleveltools import override
        start_pitch_clef = pitchtools.suggest_clef_for_named_pitches(
            self.start_pitch)
        stop_pitch_clef = pitchtools.suggest_clef_for_named_pitches(
            self.stop_pitch)
        start_note = scoretools.Note(self.start_pitch, 1)
        stop_note = scoretools.Note(self.stop_pitch, 1)
        glissando = spannertools.Glissando()
        if start_pitch_clef == stop_pitch_clef:
            if start_pitch_clef == indicatortools.Clef('bass'):
                bass_staff = scoretools.Staff()
                attach(indicatortools.Clef('bass'), bass_staff)
                bass_staff.extend([start_note, stop_note])
                attach(glissando, bass_staff.select_leaves())
                score = scoretools.Score([bass_staff])
            else:
                treble_staff = scoretools.Staff()
                attach(indicatortools.Clef('treble'), treble_staff)
                treble_staff.extend([start_note, stop_note])
                attach(glissando, treble_staff.select_leaves())
                score = scoretools.Score([treble_staff])
        else:
            result = scoretools.make_empty_piano_score()
            score, treble_staff, bass_staff = result
            bass_staff.extend([start_note, stop_note])
            treble_staff.extend(scoretools.Skip(1) * 2)
            attach(glissando, bass_staff.select_leaves())
            attach(indicatortools.StaffChange(treble_staff), bass_staff[1])
        for leaf in iterate(score).by_class(scoretools.Leaf):
            attach(durationtools.Multiplier(1, 4), leaf)
        override(score).bar_line.stencil = False
        override(score).span_bar.stencil = False
        override(score).glissando.thickness = 2
        override(score).time_signature.stencil = False
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
        lilypond_file.header_block.tagline = markuptools.Markup('""')
        return lilypond_file

    def __le__(self, arg):
        r'''Is true when stop pitch of pitch-range is less than or equal 
        to `arg`. Otherwise false.

        Returns boolean.
        '''
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedPitch(arg)
            if self.stop_pitch is None:
                return False
            return self.stop_pitch <= pitch
        except (TypeError, ValueError):
            return False

    def __lt__(self, arg):
        r'''Is true when stop pitch of pitch-range is less than `arg`. 
        Otherwise false.

        Returns boolean.
        '''
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedPitch(arg)
            if self.stop_pitch is None:
                return False
            return self.stop_pitch < pitch
        except (TypeError, ValueError):
            return False

    def __ne__(self, arg):
        r'''Is true when pitch range does not equal `arg`. Otherwise false.

        Returns boolean.
        '''
        return not self == arg

    ### PRIVATE CLASS VARIABLES ###

    _start_punctuation_to_inclusivity_string = {
        '[': 'inclusive',
        '(': 'exclusive',
        }

    _stop_punctuation_to_inclusivity_string = {
        ']': 'inclusive',
        ')': 'exclusive',
        }

    ### PRIVATE PROPERTIES ###

    @property
    def _close_bracket_string(self):
        if self.stop_pitch_is_included_in_range:
            return ']'
        else:
            return ')'

    @property
    def _one_line_menuing_summary(self):
        return self.one_line_named_pitch_repr

    @property
    def _open_bracket_string(self):
        if self.start_pitch_is_included_in_range:
            return '['
        else:
            return '('

    @property
    def _repr_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=(
                'pitch_range_name',
                'pitch_range_name_markup',
                ),
            positional_argument_values=(
                self.one_line_named_pitch_repr,
                ),
            )

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(
                'pitch_range_name',
                'pitch_range_name_markup',
                ),
            positional_argument_values=(
                self.one_line_named_pitch_repr,
                ),
            )

    ### PRIVATE METHODS ###

    def _contains_pitch(self, pitch):
        from abjad.tools import pitchtools
        if isinstance(pitch, numbers.Number):
            pitch = pitchtools.NamedPitch(pitch)
        elif isinstance(pitch, str):
            pitch = pitchtools.NamedPitch(pitch)
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

    def _initialize_by_symbolic_pitch_range_string(
        self, 
        symbolic_pitch_range_string,
        ):
        from abjad.tools import pitchtools
        match = self._symbolic_pitch_range_string_regex.match(
            symbolic_pitch_range_string)
        if match is None:
            message = 'can not instantiate pitch range: {!r}'
            message = message.format(symbolic_pitch_range_string)
            raise ValueError(message)
        groups = match.groups()
        start_punctuation = groups[0]
        start_pitch_string = groups[1]
        stop_pitch_string = groups[8]
        stop_punctuation = groups[-1]
        start_inclusivity_string = \
            self._start_punctuation_to_inclusivity_string[start_punctuation]
        stop_inclusivity_string = \
            self._stop_punctuation_to_inclusivity_string[stop_punctuation]
        start_pair = (start_pitch_string, start_inclusivity_string)
        stop_pair = (stop_pitch_string, stop_inclusivity_string)
        type(self).__init__(self, start_pair, stop_pair)

    ### PUBLIC METHODS ###

    @classmethod
    def is_symbolic_pitch_range_string(cls, expr):
        '''Is true when `expr` is a symbolic pitch range string. 
        Otherwise false:

        ::

            >>> pitchtools.PitchRange.is_symbolic_pitch_range_string(
            ...     '[A0, C8]')
            True

        The regex that underlies this predicate matches against two
        comma-separated pitches enclosed in some combination of square
        brackets and round parentheses.

        Returns boolean.
        '''
        if not isinstance(expr, str):
            return False
        return bool(cls._symbolic_pitch_range_string_regex.match(expr))

    ### PUBLIC PROPERTIES ###

    @property
    def one_line_named_pitch_repr(self):
        r'''One-line named pitch representation of pitch range.

        ::

            >>> pitch_range.one_line_named_pitch_repr
            '[C3, C7]'

        Returns string.
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
    def one_line_numbered_pitch_repr(self):
        r'''One-line numbered pitch representation of pitch range.

        ::

            >>> pitch_range.one_line_numbered_pitch_repr
            '[-12, 36]'

        Returns string.
        '''
        result = []
        result.append(self._open_bracket_string)
        result.append(str(self.start_pitch.pitch_number))
        result.append(', ')
        result.append(str(self.stop_pitch.pitch_number))
        result.append(self._close_bracket_string)
        result = ''.join(result)
        return result

    # TODO: change to custom_identifier or remove altogether
    @property
    def pitch_range_name(self):
        r'''Name of pitch range.

        ::

            >>> pitch_range.pitch_range_name
            'four-octave range'

        Returns string or none.
        '''
        return self._pitch_range_name
            
    # TODO: change to custom_identifier_markup or remove altogether
    @property
    def pitch_range_name_markup(self):
        r'''Pitch range name markup.

        ::

            >>> pitch_range.pitch_range_name_markup
            Markup(contents=('four-octave range',))

        Default to `pitch_range_name` when `pitch_range_name_markup`
        not set explicitly.

        Returns markup or none.
        '''
        from abjad.tools import markuptools
        if self._pitch_range_name_markup:
            return self._pitch_range_name_markup
        elif self.pitch_range_name:
            return markuptools.Markup(self.pitch_range_name)

    @property
    def start_pitch(self):
        r'''Start pitch of pitch range.

        ::

            >>> pitch_range.start_pitch
            NamedPitch('c')

        Returns pitch.
        '''
        if self._start is None:
            return None
        return self._start[0]

    @property
    def start_pitch_is_included_in_range(self):
        r'''Is true when start pitch is included in range.
        Otherwise false:

        ::

            >>> pitch_range.start_pitch_is_included_in_range
            True

        Returns boolean.
        '''
        if self._start is None:
            return True
        return self._start[1] == 'inclusive'

    @property
    def stop_pitch(self):
        r"""Stop pitch of pitch range.

        ::

            >>> pitch_range.stop_pitch
            NamedPitch("c''''")

        Returns pitch.
        """
        if self._stop is None:
            return None
        return self._stop[0]

    @property
    def stop_pitch_is_included_in_range(self):
        r'''Is true when stop pitch is included in range.
        Otherwise false:

        ::

            >>> pitch_range.stop_pitch_is_included_in_range
            True

        Returns boolean.
        '''
        if self._stop is None:
            return True
        return self._stop[1] == 'inclusive'
