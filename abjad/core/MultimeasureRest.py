import typing

from abjad import typings
from abjad.system.Tag import Tag

from .Leaf import Leaf
from .Rest import Rest


class MultimeasureRest(Leaf):
    r"""
    Multimeasure rest.

    ..  container:: example

        >>> rest = abjad.MultimeasureRest((1, 4))
        >>> abjad.show(rest) # doctest: +SKIP

    ..  container:: example

        Multimeasure rests may be tagged:

        >>> rest = abjad.MultimeasureRest(
        ...     'R1', tag=abjad.Tag('GLOBAL_MULTIMEASURE_REST')
        ... )
        >>> abjad.f(rest)
        R1 %! GLOBAL_MULTIMEASURE_REST

    ..  container:: example

        REGRESSION #1049. Parser reads multimeasure rest multipliers:

        >>> staff = abjad.Staff(r"\time 3/8 R1 * 3/8")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \time 3/8
                R1 * 3/8
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Leaves"

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self, *arguments, multiplier: typings.DurationTyping = None, tag: Tag = None,
    ) -> None:
        if len(arguments) == 0:
            arguments = ((1, 4),)
        rest = Rest(*arguments)
        Leaf.__init__(self, rest.written_duration, multiplier=multiplier, tag=tag)

    ### PRIVATE METHODS ###

    def _get_body(self):
        """
        Gets list of string representation of body of rest.
        Picked up as format contribution at format-time.
        """
        result = "R" + str(self._get_formatted_duration())
        return [result]

    def _get_compact_representation(self):
        return f"R{self._get_formatted_duration()}"

    ### PUBLIC PROPERTIES ###

    @property
    def tag(self) -> typing.Optional[Tag]:
        r"""
        Gets tag.

        ..  container:: example

            >>> rest = abjad.MultimeasureRest(
            ...     1, tag=abjad.Tag('MULTIMEASURE_REST')
            ... )
            >>> rest.multiplier = (3, 8)

            >>> abjad.f(rest)
            R1 * 3/8 %! MULTIMEASURE_REST

        """
        return super().tag
