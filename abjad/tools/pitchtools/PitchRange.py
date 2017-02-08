# -*- coding: utf-8 -*-
import collections
import copy
import numbers
import re
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.pitchtools.Pitch import Pitch
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import select


# TODO: make iterable so that for x in PitchRange works
class PitchRange(AbjadValueObject):
    r"""Pitch range.

    ..  container:: example

        Pitches from C3 to C7, inclusive:

        ::

            >>> pitch_range = PitchRange('[C3, C7]')
            >>> f(pitch_range)
            pitchtools.PitchRange(
                range_string='[C3, C7]',
                )

        ::

            >>> show(pitch_range) # doctest: +SKIP

    Initalizes from pitch numbers, pitch names, pitch instances,
    one-line reprs or other pitch range objects.

    Pitch ranges implement equality testing against other pitch ranges.

    Pitch ranges test less than, greater than, less-equal and
    greater-equal against pitches.

    Pitch ranges do not sort relative to other pitch ranges.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start',
        '_stop',
        )

    _publish_storage_format = True

    _range_string_regex_body = '''
        (?P<open_bracket>
            [\[(]       # open bracket or open parenthesis
        )
        (?P<start_pitch>
            {}|{}|-?\d+ # start pitch
        )
        ,               # comma
        [ ]*            # any amount of whitespace
        (?P<stop_pitch>
            {}|{}|-?\d+ # stop pitch
        )
        (?P<close_bracket>
            [\])]       # close bracket or close parenthesis
        )
        '''.format(
        Pitch._pitch_class_octave_number_regex_body.replace('<', '<start_'),
        Pitch._pitch_name_regex_body.replace('<', '<start_'),
        Pitch._pitch_class_octave_number_regex_body.replace('<', '<stop_'),
        Pitch._pitch_name_regex_body.replace('<', '<stop_'),
        )

    _range_string_regex = re.compile(
        '^{}$'.format(_range_string_regex_body),
        re.VERBOSE,
        )

    _start_punctuation_to_inclusivity_string = {
        '[': 'inclusive',
        '(': 'exclusive',
        }

    _stop_punctuation_to_inclusivity_string = {
        ']': 'inclusive',
        ')': 'exclusive',
        }

    ### INITIALIZER ###

    def __init__(self, range_string='[A0, C8]'):
        start, stop = self._parse_range_string(range_string)
        self._start = start
        self._stop = stop

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        r'''Is true when pitch range contains `argument`. Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        if (
            hasattr(argument, '_has_effective_indicator') and
            'unpitched' in inspect_(argument).get_indicators(str)
            ):
            return True
        elif isinstance(argument, (int, float)):
            pitch = pitchtools.NamedPitch(argument)
            return self._contains_pitch(pitch)
        elif isinstance(argument, pitchtools.NamedPitch):
            return self._contains_pitch(argument)
        elif isinstance(argument, scoretools.Note):
            sounding_pitch = inspect_(argument).get_sounding_pitch()
            return self._contains_pitch(sounding_pitch)
        elif isinstance(argument, scoretools.Chord):
            sounding_pitches = inspect_(argument).get_sounding_pitches()
            return all(self._contains_pitch(x) for x in sounding_pitches)
            try:
                argument = type(self)(argument)
                return self.__lt__(argument)
            except TypeError:
                pass
        elif isinstance(argument, (scoretools.Rest, scoretools.Skip)):
            return True
        elif isinstance(argument, scoretools.Container):
            return all(x in self for x in iterate(argument).by_leaf())
        else:
            pitches = list(iterate(argument).by_pitch())
            if pitches:
                return all(self._contains_pitch(x) for x in pitches)
            else:
                try:
                    return all(self._contains_pitch(x) for x in argument)
                except TypeError:
                    return False
        return False

    def __eq__(self, argument):
        r'''Is true when `argument` is a pitch range with start and stop equal
        to those of this pitch range. Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import systemtools
        return systemtools.TestManager.compare_objects(self, argument)

    def __format__(self, format_specification=''):
        r'''Formats pitch range.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __ge__(self, argument):
        r'''Is true when start pitch of pitch range is greater than or equal to
        `argument`. Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedPitch(argument)
            if self.start_pitch is None:
                return False
            return pitch <= self.start_pitch
        except (TypeError, ValueError):
            return False

    def __gt__(self, argument):
        r'''Is true when start pitch of pitch range is greater than `argument`.
        Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedPitch(argument)
            if self.start_pitch is None:
                return False
            return pitch < self.start_pitch
        except (TypeError, ValueError):
            return False

    def __hash__(self):
        r'''Hashes pitch range.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatAgent(self).get_hash_values()
        return hash(hash_values)

    def __illustrate__(self):
        r'''Illustrates pitch range.

        ::

            >>> show(pitch_range) # doctest: +SKIP

        Returns LilyPond file.
        '''
        import abjad
        start_pitch_clef = abjad.Clef.from_selection(self.start_pitch)
        stop_pitch_clef = abjad.Clef.from_selection(self.stop_pitch)
        start_note = abjad.Note(self.start_pitch, 1)
        stop_note = abjad.Note(self.stop_pitch, 1)
        glissando = abjad.Glissando()
        if start_pitch_clef == stop_pitch_clef:
            if start_pitch_clef == abjad.Clef('bass'):
                bass_staff = abjad.Staff()
                abjad.attach(abjad.Clef('bass'), bass_staff)
                bass_staff.extend([start_note, stop_note])
                bass_leaves = select(bass_staff).by_leaf()
                abjad.attach(glissando, bass_leaves)
                score = abjad.Score([bass_staff])
            else:
                treble_staff = abjad.Staff()
                abjad.attach(abjad.Clef('treble'), treble_staff)
                treble_staff.extend([start_note, stop_note])
                treble_leaves = select(treble_staff).by_leaf()
                abjad.attach(glissando, treble_leaves)
                score = abjad.Score([treble_staff])
        else:
            result = abjad.scoretools.make_empty_piano_score()
            score, treble_staff, bass_staff = result
            bass_staff.extend([start_note, stop_note])
            treble_staff.extend(abjad.Skip(1) * 2)
            bass_leaves = select(bass_staff).by_leaf()
            abjad.attach(glissando, bass_leaves)
            abjad.attach(abjad.StaffChange(treble_staff), bass_staff[1])
        for leaf in abjad.iterate(score).by_leaf():
            abjad.attach(abjad.Multiplier(1, 4), leaf)
        abjad.override(score).bar_line.stencil = False
        abjad.override(score).span_bar.stencil = False
        abjad.override(score).glissando.thickness = 2
        abjad.override(score).time_signature.stencil = False
        lilypond_file = abjad.LilyPondFile.new(score)
        lilypond_file.header_block.tagline = False
        return lilypond_file

    def __le__(self, argument):
        r'''Is true when stop pitch of pitch-range is less than or equal
        to `argument`. Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedPitch(argument)
            if self.stop_pitch is None:
                return False
            return self.stop_pitch <= pitch
        except (TypeError, ValueError):
            return False

    def __lt__(self, argument):
        r'''Is true when stop pitch of pitch-range is less than `argument`.
        Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedPitch(argument)
            if self.stop_pitch is None:
                return False
            return self.stop_pitch < pitch
        except (TypeError, ValueError):
            return False

    def __ne__(self, argument):
        r'''Is true when pitch range does not equal `argument`. Otherwise false.

        Returns true or false.
        '''
        return not self == argument

    ### PRIVATE PROPERTIES ###

    @property
    def _close_bracket_string(self):
        if self.stop_pitch_is_included_in_range:
            return ']'
        else:
            return ')'

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
            pitch = pitchtools.NamedPitch(pitch)
        elif isinstance(pitch, str):
            pitch = pitchtools.NamedPitch(pitch)
        if self.start_pitch is None and self.stop_pitch is None:
            return True
        elif self.start_pitch is None:
            if self.stop_pitch_is_included_in_range:
                return pitch <= self.stop_pitch
            else:
                return pitch < self.stop_pitch
        elif self.stop_pitch is None:
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

    def _get_named_range_string(self):
        result = []
        result.append(self._open_bracket_string)
        if self.start_pitch:
            result.append(self.start_pitch.pitch_class_octave_label)
        else:
            result.append('-inf')
        result.append(', ')
        if self.stop_pitch:
            result.append(self.stop_pitch.pitch_class_octave_label)
        else:
            result.append('+inf')
        result.append(self._close_bracket_string)
        result = ''.join(result)
        return result

    def _get_numbered_range_string(self):
        result = []
        result.append(self._open_bracket_string)
        result.append(str(self.start_pitch.pitch_number))
        result.append(', ')
        result.append(str(self.stop_pitch.pitch_number))
        result.append(self._close_bracket_string)
        result = ''.join(result)
        return result

    def _list_numeric_octave_transpositions(self, pitch_number_list):
        result = []
        pitch_number_set = set(pitch_number_list)
        start_pitch_number = self.start_pitch.pitch_number
        stop_pitch_number = self.stop_pitch.pitch_number
        range_set = set(range(start_pitch_number, stop_pitch_number + 1))
        while pitch_number_set.issubset(range_set):
            next_pitch_number = list(pitch_number_set)
            next_pitch_number.sort()
            result.extend([next_pitch_number])
            pitch_number_set = set([_ + 12 for _ in pitch_number_set])
        pitch_number_set = set([_ - 12 for _ in pitch_number_list])
        while pitch_number_set.issubset(range_set):
            next_pitch_number = list(pitch_number_set)
            next_pitch_number.sort()
            result.extend([next_pitch_number])
            pitch_number_set = set([_ - 12 for _ in pitch_number_set])
        result.sort()
        return result

    def _parse_range_string(self, range_string):
        from abjad.tools import pitchtools
        assert isinstance(range_string, str), repr(range_string)
        range_string = range_string.replace('-inf', '-1000')
        range_string = range_string.replace('+inf', '1000')
        match = self._range_string_regex.match(range_string)
        if match is None:
            message = 'can not instantiate pitch range: {!r}'
            message = message.format(range_string)
            raise ValueError(message)
        group_dict = match.groupdict()
        start_punctuation = group_dict['open_bracket']
        start_pitch_string = group_dict['start_pitch']
        stop_pitch_string = group_dict['stop_pitch']
        stop_punctuation = group_dict['close_bracket']
        start_inclusivity_string = \
            self._start_punctuation_to_inclusivity_string[start_punctuation]
        stop_inclusivity_string = \
            self._stop_punctuation_to_inclusivity_string[stop_punctuation]
        if start_pitch_string == '-1000':
            start_pitch = None
        else:
            try:
                start_pitch = pitchtools.NamedPitch(start_pitch_string)
            except TypeError:
                start_pitch = pitchtools.NumberedPitch(int(start_pitch_string))
        if stop_pitch_string == '1000':
            stop_pitch = None
        else:
            try:
                stop_pitch = pitchtools.NamedPitch(stop_pitch_string)
            except TypeError:
                stop_pitch = pitchtools.NumberedPitch(int(stop_pitch_string))
        start_pair = (start_pitch, start_inclusivity_string)
        stop_pair = (stop_pitch, stop_inclusivity_string)
        return start_pair, stop_pair

    ### PUBLIC PROPERTIES ###

    @property
    def range_string(self):
        r'''Gets range string of pitch range.

        ..  container:: example

            ::

                >>> pitch_range.range_string
                '[C3, C7]'

        Returns string.
        '''
        return self._get_named_range_string()

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

        Returns true or false.
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

        Returns true or false.
        '''
        if self._stop is None:
            return True
        return self._stop[1] == 'inclusive'

    ### PUBLIC METHODS ###

    @staticmethod
    def from_pitches(
        start_pitch,
        stop_pitch,
        start_pitch_is_included_in_range=True,
        stop_pitch_is_included_in_range=True,
        ):
        r'''Initializes pitch range from numbers.

        ..  container:: example

            ::

                >>> PitchRange.from_pitches(-18, 19)
                PitchRange(range_string='[F#2, G5]')

        Returns pitch range.
        '''
        from abjad.tools import pitchtools
        if start_pitch is None:
            start_pitch_string = '-inf'
        else:
            start_pitch_string = str(pitchtools.NamedPitch(start_pitch))
        if stop_pitch is None:
            stop_pitch_string = '+inf'
        else:
            stop_pitch_string = str(pitchtools.NamedPitch(stop_pitch))
        start_containment = '['
        if not start_pitch_is_included_in_range:
            start_containment = '('
        stop_containment = ']'
        if not stop_pitch_is_included_in_range:
            stop_containment = ')'
        string = '{}{}, {}{}'
        string = string.format(
            start_containment,
            start_pitch_string,
            stop_pitch_string,
            stop_containment,
            )
        pitch_range = PitchRange(string)
        return pitch_range

    @classmethod
    def is_range_string(class_, argument):
        '''Is true when `argument` is a symbolic pitch range string.
        Otherwise false:

        ..  container:: example

            Returns true:

            ::

                >>> PitchRange.is_range_string('[A0, C8]')
                True

        ..  container:: example

            Returns false:

            ::

                >>> PitchRange.is_range_string('text')
                False

        The regex that underlies this predicate matches against two
        comma-separated pitches enclosed in some combination of square
        brackets and round parentheses.

        Returns true or false.
        '''
        if not isinstance(argument, str):
            return False
        return bool(class_._range_string_regex.match(argument))

    def list_octave_transpositions(self, pitch_carrier):
        r"""Lists octave transpositions of `pitch_carrier` in pitch range.

        ..  container:: example

            Lists octave transpositions of three-pitch chord:

            ::

                >>> chord = Chord("<c' d' e'>4")
                >>> pitch_range = PitchRange.from_pitches(0, 48)
                >>> result = pitch_range.list_octave_transpositions(chord)

            ::

                >>> for chord in result:
                ...     chord
                ...
                Chord("<c' d' e'>4")
                Chord("<c'' d'' e''>4")
                Chord("<c''' d''' e'''>4")
                Chord("<c'''' d'''' e''''>4")

        Returns a list of `pitch_carrier` objects.
        """
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        if isinstance(pitch_carrier, collections.Iterable):
            if all(isinstance(x, (int, float)) for x in pitch_carrier):
                return self._list_numeric_octave_transpositions(pitch_carrier)
        prototype = (scoretools.Chord, pitchtools.PitchSet)
        if not isinstance(pitch_carrier, prototype):
            message = 'must be chord or pitch-set: {!r}'
            message = message.format(pitch_carrier)
            raise TypeError(message)
        result = []
        interval = pitchtools.NumberedInterval(-12)
        while True:
            pitch_carrier_copy = copy.copy(pitch_carrier)
            candidate = interval.transpose(pitch_carrier_copy)
            if candidate in self:
                result.append(candidate)
                interval -= pitchtools.NumberedInterval(12)
            else:
                break
        result.reverse()
        interval = pitchtools.NumberedInterval(0)
        while True:
            pitch_carrier_copy = copy.copy(pitch_carrier)
            candidate = interval.transpose(pitch_carrier_copy)
            if candidate in self:
                result.append(candidate)
                interval += pitchtools.NumberedInterval(12)
            else:
                break
        return result

    def voice_pitch_class(self, pitch_class):
        r"""Voices `pitch_class`:

        ..  container:: example

            Voices C three times:

            ::

                >>> pitch_range = PitchRange('[C4, C6]')
                >>> pitch_range.voice_pitch_class('c')
                (NamedPitch("c'"), NamedPitch("c''"), NamedPitch("c'''"))

        ..  container:: example

            Voices B two times:

            ::

                >>> pitch_range = PitchRange('[C4, C6]')
                >>> pitch_range.voice_pitch_class('b')
                (NamedPitch("b'"), NamedPitch("b''"))

        ..  container:: example

            Returns empty because B can not voice:

            ::

                >>> pitch_range = PitchRange('[C4, A4)')
                >>> pitch_range.voice_pitch_class('b')
                ()

        Returns tuple of zero or more named pitches.
        """
        from abjad.tools import pitchtools
        named_pitch_class = pitchtools.NamedPitchClass(pitch_class)
        named_pitch = pitchtools.NamedPitch(
            named_pitch_class,
            self.start_pitch.octave.number,
            )
        result = []
        while named_pitch <= self.stop_pitch:
            if named_pitch in self:
                result.append(named_pitch)
            named_pitch += 12
        return tuple(result)
