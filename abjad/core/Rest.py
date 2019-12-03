from abjad import typings
from abjad.system.Tag import Tag
from abjad.top.parse import parse
from abjad.utilities.Duration import Duration

from .Leaf import Leaf


class Rest(Leaf):
    r"""
    Rest.

    ..  container:: example

        >>> rest = abjad.Rest('r8.')
        >>> abjad.attach(abjad.TimeSignature((3, 16)), rest)
        >>> staff = abjad.Staff([rest])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \time 3/16
                r8.
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Leaves"

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        written_duration=None,
        *,
        multiplier: typings.DurationTyping = None,
        tag: Tag = None,
    ) -> None:
        original_input = written_duration
        if isinstance(written_duration, Leaf):
            multiplier = written_duration.multiplier
        if isinstance(written_duration, str):
            string = f"{{ {written_duration} }}"
            parsed = parse(string)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            written_duration = parsed[0]
        if isinstance(written_duration, Leaf):
            written_duration = written_duration.written_duration
        elif written_duration is None:
            written_duration = Duration(1, 4)
        else:
            written_duration = Duration(written_duration)
        Leaf.__init__(self, written_duration, multiplier=multiplier, tag=tag)
        if isinstance(original_input, Leaf):
            self._copy_override_and_set_from_leaf(original_input)

    ### PRIVATE METHODS ###

    def _get_body(self):
        return [self._get_compact_representation()]

    def _get_compact_representation(self):
        return f"r{self._get_formatted_duration()}"
