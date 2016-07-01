# -*- coding: utf-8 -*-
import numbers
from abjad.tools.pitchtools.NamedIntervalClass import NamedIntervalClass


class NamedInversionEquivalentIntervalClass(NamedIntervalClass):
    '''Named inversion-equivalent interval-class.

    ..  container:: example

        **Example 1.** Initializes from string:

        ::

            >>> pitchtools.NamedInversionEquivalentIntervalClass('-m14')
            NamedInversionEquivalentIntervalClass('+M2')

    Named inversion-equivalent interval-classes are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        '_quality_string',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import pitchtools
        if len(args) == 1 and isinstance(args[0], type(self)):
            self._initialize_by_self_reference(args[0])
        elif len(args) == 1 and isinstance(args[0], str):
            self._initialize_by_string(args[0])
        elif len(args) == 1 and isinstance(args[0],
            pitchtools.NamedIntervalClass):
            self._initialize_by_string(str(args[0]))
        elif len(args) == 1 and isinstance(args[0],
            pitchtools.NamedInterval):
            interval_class = pitchtools.NamedIntervalClass(args[0])
            self._initialize_by_string(str(interval_class))
        elif len(args) == 1 and isinstance(args[0], tuple):
            self._initialize_by_quality_string_and_number(*args[0])
        elif len(args) == 2:
            self._initialize_by_quality_string_and_number(*args)
        elif len(args) == 0:
            self._initialize_by_string('P1')
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, args)
            raise ValueError(message)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        r'''Is true when `arg` is a named inversion-equivalent interval-class with
        quality string and number equal to those of this named
        inversion-equivalent interval-class. Otherwise false.

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            if self.quality_string == arg.quality_string:
                if self.number == arg.number:
                    return True
        return False

    def __hash__(self):
        r'''Required to be explicitly redefined on Python 3 if
        __eq__ changes

        Returns integer.
        '''
        return super(NamedInversionEquivalentIntervalClass, self).__hash__()

    def __ne__(self, arg):
        r'''Is true when named inversion-equivalent interval-class does not equal
        `arg`. Otherwise false.

        Returns true or false.
        '''
        return not self == arg

    ### PRIVATE METHODS ###

    def _initialize_by_quality_string_and_number(self, quality_string, number):
        if number == 0:
            message = 'named interval can not equal zero.'
            raise ValueError(message)
        elif abs(number) == 1:
            number = 1
        elif abs(number) % 7 == 0:
            number = 7
        elif abs(number) % 7 == 1:
            number = 8
        else:
            number = abs(number) % 7
        if self._is_representative_number(number):
            quality_string = quality_string
            number = number
        else:
            quality_string = self._invert_quality_string(quality_string)
            number = 9 - number
        self._quality_string = quality_string
        self._number = number

    def _initialize_by_self_reference(self, reference):
        quality_string = reference.quality_string
        number = reference.number
        self._initialize_by_quality_string_and_number(quality_string, number)

    def _initialize_by_string(self, string):
        from abjad.tools import pitchtools
        match = pitchtools.Interval._interval_name_abbreviation_regex.match(string)
        if match is None:
            raise ValueError(
                '{!r} does not have the form of a hdi abbreviation.'.format(
                string))
        direction_string, quality_abbreviation, number_string = \
            match.groups()
        quality_string = self._quality_abbreviation_to_quality_string[
            quality_abbreviation]
        number = int(number_string)
        self._initialize_by_quality_string_and_number(quality_string, number)

    def _invert_quality_string(self, quality_string):
        inversions = {
            'major': 'minor',
            'minor': 'major',
            'perfect': 'perfect',
            'augmented': 'diminished',
            'diminished': 'augmented',
            }
        return inversions[quality_string]

    def _is_representative_number(self, arg):
        if isinstance(arg, numbers.Number):
            if 1 <= arg <= 4 or arg == 8:
                return True
        return False

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
        '''Makes named inversion-equivalent interval-class from
        `pitch_carrier_1` and `pitch_carrier_2`.

        ::

            >>> pitchtools.NamedInversionEquivalentIntervalClass.from_pitch_carriers(
            ...     NamedPitch(-2),
            ...     NamedPitch(12),
            ...     )
            NamedInversionEquivalentIntervalClass('+M2')

        Returns named inversion-equivalent interval-class.
        '''
        from abjad.tools import pitchtools
        named_interval = pitchtools.NamedInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2)
        return class_(named_interval)
