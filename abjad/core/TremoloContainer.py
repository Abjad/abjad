from abjad import mathtools
from abjad.utilities.Multiplier import Multiplier
from .Container import Container


class TremoloContainer(Container):
    r"""
    Tremolo container.

    ..  container:: example

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.TremoloContainer(2, "c'16 e'"))
        >>> staff.append("cs'4")
        >>> staff.append(abjad.TremoloContainer(2, "d'16 f'"))
        >>> staff.append("ds'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \repeat tremolo 2 {
                    c'16
                    e'16
                }
                cs'4
                \repeat tremolo 2 {
                    d'16
                    f'16
                }
                ds'4
            }

        Duration of container equal to contents duration multiplied by count:

        >>> abjad.inspect(staff[0]).duration()
        Duration(1, 4)

        Duration of each leaf equal to written duration multiplied by count:

        >>> abjad.inspect(staff[0][0]).duration()
        Duration(1, 8)

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Containers"

    __slots__ = ("_count",)

    ### INITIALIZER ###

    def __init__(
        self, count: int = 2, components=None, *, tag: str = None
    ) -> None:
        assert mathtools.is_assignable_integer(count), repr(count)
        self._count = count
        Container.__init__(self, components, tag=tag)
        if len(self) != 2:
            raise Exception(f"must contain 2 leaves (not {len(self)}")

    ### SPECIAL METHODS ###

    def __getnewargs__(self) -> tuple:
        """
        Gets new arguments of tremolo container.
        """
        return (self.count,)

    ### PRIVATE METHODS ###

    def _format_open_brackets_slot(self, bundle):
        result = []
        string = rf"\repeat tremolo {self.count} {{"
        result.append([("tremolo_brackets", "open"), [string]])
        return tuple(result)

    def _get_lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()

    def _get_preprolated_duration(self):
        return self.implied_prolation * self._get_contents_duration()

    ### PUBLIC PROPERTIES ###

    @property
    def count(self) -> int:
        """
        Gets count.

        ..  container:: example

            >>> tremolo_container = abjad.TremoloContainer(2, "<c' d'>16 e'16")
            >>> tremolo_container.count
            2

        """
        return self._count

    @property
    def implied_prolation(self) -> Multiplier:
        r"""
        Gets implied prolation of tremolo container.

        ..  container:: example

            Defined equal to count.

            >>> tremolo_container = abjad.TremoloContainer(2, "<c' d'>16 e'16")
            >>> abjad.show(tremolo_container) # doctest: +SKIP

            >>> tremolo_container.implied_prolation
            Multiplier(2, 1)

        """
        multiplier = Multiplier(self.count)
        return multiplier
