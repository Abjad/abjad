import functools
import typing
from abjad.mathtools.NonreducedFraction import NonreducedFraction
from abjad.system.FormatSpecification import FormatSpecification
from .Scheme import Scheme


@functools.total_ordering
class SchemeMoment(Scheme):
    """
    Abjad model of Scheme moment.

    ..  container:: example

        Initializes with two integers:

        >>> abjad.SchemeMoment((2, 68))
        SchemeMoment((2, 68))

    Scheme moments are immutable.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        duration: typing.Union[typing.Tuple[int, int]] = (0, 1),
        ) -> None:
        pair = NonreducedFraction(duration).pair
        Scheme.__init__(self, pair)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a scheme moment with the same value as
        that of this scheme moment.

        ..  container:: example

            >>> abjad.SchemeMoment((2, 68)) == abjad.SchemeMoment((2, 68))
            True

        ..  container:: example

            Otherwise false:

            >>> abjad.SchemeMoment((2, 54)) == abjad.SchemeMoment((2, 68))
            False

        """
        return super(SchemeMoment, self).__eq__(argument)

    def __hash__(self) -> int:
        """
        Hashes scheme moment.

        Redefined in tandem with ``__eq__``.
        """
        return super(SchemeMoment, self).__hash__()

    def __lt__(self, argument) -> bool:
        """
        Is true when ``argument`` is a scheme moment with value greater than
        that of this scheme moment.

        ..  container:: example

            >>> abjad.SchemeMoment((1, 68)) < abjad.SchemeMoment((1, 32))
            True

        ..  container:: example

            Otherwise false:

            >>> abjad.SchemeMoment((1, 68)) < abjad.SchemeMoment((1, 78))
            False

        """
        if isinstance(argument, type(self)):
            if self.duration < argument.duration:
                return True
        return False

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.value]
        return FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_kwargs_names=[],
            )

    def _get_formatted_value(self):
        pair = self.duration.pair
        string = f'(ly:make-moment {pair[0]} {pair[1]})'
        return string

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self) -> NonreducedFraction:
        """
        Gets duration of Scheme moment.

        ..  container:: example

            >>> abjad.SchemeMoment((2, 68)).duration
            NonreducedFraction(2, 68)

        """
        return NonreducedFraction(self.value)
