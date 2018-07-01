import numbers
from .NamedIntervalClass import NamedIntervalClass


class NamedInversionEquivalentIntervalClass(NamedIntervalClass):
    """
    Named inversion-equivalent interval-class.

    ..  container:: example

        Initializes from string:

        >>> abjad.NamedInversionEquivalentIntervalClass('-m14')
        NamedInversionEquivalentIntervalClass('+M2')

    ..  container:: example

        Initializes from pair:

        >>> abjad.NamedInversionEquivalentIntervalClass(('perfect', 1))
        NamedInversionEquivalentIntervalClass('P1')

        >>> abjad.NamedInversionEquivalentIntervalClass(('perfect', -1))
        NamedInversionEquivalentIntervalClass('P1')

        >>> abjad.NamedInversionEquivalentIntervalClass(('augmented', 4))
        NamedInversionEquivalentIntervalClass('+A4')

        >>> abjad.NamedInversionEquivalentIntervalClass(('augmented', -4))
        NamedInversionEquivalentIntervalClass('+A4')

        >>> abjad.NamedInversionEquivalentIntervalClass(('augmented', 11))
        NamedInversionEquivalentIntervalClass('+A4')

        >>> abjad.NamedInversionEquivalentIntervalClass(('augmented', -11))
        NamedInversionEquivalentIntervalClass('+A4')

    ..  container:: example

        Initializes from other interval-class:

        >>> interval_class = abjad.NamedInversionEquivalentIntervalClass(
        ...     'P1',
        ...     )
        >>> abjad.NamedInversionEquivalentIntervalClass(interval_class)
        NamedInversionEquivalentIntervalClass('P1')

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, name='P1'):
        super().__init__(name or 'P1')
        self._quality, self._number = self._process_quality_and_number(
            self._quality,
            self._number,
            )

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when `argument` is a named inversion-equivalent
        interval-class with name equal to that of this named
        inversion-equivalent interval-class.

        ..  container:: example

            >>> class_ = abjad.NamedInversionEquivalentIntervalClass
            >>> interval_class_1 = class_('P1')
            >>> interval_class_2 = class_('P1')
            >>> interval_class_3 = class_('m2')

            >>> interval_class_1 == interval_class_1
            True
            >>> interval_class_1 == interval_class_2
            True
            >>> interval_class_1 == interval_class_3
            False

            >>> interval_class_2 == interval_class_1
            True
            >>> interval_class_2 == interval_class_2
            True
            >>> interval_class_2 == interval_class_3
            False

            >>> interval_class_3 == interval_class_1
            False
            >>> interval_class_3 == interval_class_2
            False
            >>> interval_class_3 == interval_class_3
            True

        Returns true or false.
        """
        return super().__eq__( argument)

    def __hash__(self):
        """
        Hashes named inversion-equivalent interval-class.

        Returns integer.
        """
        return super().__hash__()

    ### PRIVATE METHODS ###

    @classmethod
    def _invert_quality_string(class_, quality):
        inversions = {'M': 'm', 'm': 'M', 'P': 'P'}
        if quality in inversions:
            return inversions[quality]
        if quality[0] == 'A':
            return 'd' * len(quality)
        return 'A' * len(quality)

    @classmethod
    def _is_representative_number(class_, argument):
        if isinstance(argument, numbers.Number):
            if 1 <= argument <= 4 or argument == 8:
                return True
        return False

    @classmethod
    def _process_quality_and_number(class_, quality, number):
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
        if class_._is_representative_number(number):
            quality = quality
            number = number
        else:
            quality = class_._invert_quality_string(quality)
            number = 9 - number
        return quality, number

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(class_, pitch_carrier_1, pitch_carrier_2):
        """
        Makes named inversion-equivalent interval-class from
        `pitch_carrier_1` and `pitch_carrier_2`.

        ..  container:: example

            >>> class_ = abjad.NamedInversionEquivalentIntervalClass
            >>> class_.from_pitch_carriers(
            ...     abjad.NamedPitch(-2),
            ...     abjad.NamedPitch(12),
            ...     )
            NamedInversionEquivalentIntervalClass('+M2')

        Returns new named inversion-equivalent interval-class.
        """
        import abjad
        named_interval = abjad.NamedInterval.from_pitch_carriers(
            pitch_carrier_1,
            pitch_carrier_2,
            )
        string = str(named_interval)
        return class_(string)
