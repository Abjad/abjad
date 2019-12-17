import collections
import numbers
import typing

from abjad import mathtools
from abjad.system.Tag import Tag
from abjad.utilities.Duration import Duration
from abjad.utilities.Multiplier import Multiplier
from abjad.utilities.Sequence import Sequence

from .LeafMaker import LeafMaker
from .Note import Note
from .Selection import Selection


class NoteMaker(object):
    r"""
    Note-maker.

    Makes notes according to ``pitches`` and ``durations``.

    ..  container:: example

        Cycles through ``pitches`` when the length of ``pitches`` is less than
        the length of ``durations``:

        >>> maker = abjad.NoteMaker()
        >>> notes = maker([0], [(1, 16), (1, 8), (1, 8)])
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'16
                c'8
                c'8
            }

    ..  container:: example

        Cycles through ``durations`` when the length of ``durations`` is less
        than the length of ``pitches``:

        >>> maker = abjad.NoteMaker()
        >>> notes = maker(
        ...     [0, 2, 4, 5, 7],
        ...     [(1, 16), (1, 8), (1, 8)],
        ...     )
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'16
                d'8
                e'8
                f'16
                g'8
            }

    ..  container:: example

        Creates ad hoc tuplets for nonassignable durations:

        >>> maker = abjad.NoteMaker()
        >>> notes = maker([0], [(1, 16), (1, 12), (1, 8)])
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'16
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    c'8
                }
                c'8
            }

    ..  container:: example

        Set ``increase_monotonic=False`` to express tied values in decreasing
        duration:

        >>> maker = abjad.NoteMaker(increase_monotonic=False)
        >>> notes = maker([0], [(13, 16)])
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'2.
                ~
                c'16
            }

    ..  container:: example

        Set ``increase_monotonic=True`` to express tied values in increasing
        duration:

        >>> maker = abjad.NoteMaker(increase_monotonic=True)
        >>> notes = maker([0], [(13, 16)])
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'16
                ~
                c'2.
            }

    ..  container:: example

        Works with pitch segments:

        >>> maker = abjad.NoteMaker()
        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> notes = maker(segment, [(1, 8)])
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                bf8
                bqf8
                fs'8
                g'8
                bqf8
                g'8
            }

    Set ``pitches`` to a single pitch or a sequence of pitches.

    Set ``durations`` to a single duration or a list of durations.

    Returns selection.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Makers"

    __slots__ = ("_increase_monotonic", "_tag")

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, *, increase_monotonic: bool = None, tag: Tag = None) -> None:
        if increase_monotonic is not None:
            increase_monotonic = bool(increase_monotonic)
        self._increase_monotonic = increase_monotonic
        if tag is not None:
            assert isinstance(tag, Tag), repr(tag)
        self._tag = tag

    ### SPECIAL METHODS ###

    def __call__(self, pitches, durations) -> Selection:
        """
        Calls note-maker on ``pitches`` and ``durations``.
        """
        from .Tuplet import Tuplet

        if isinstance(pitches, str):
            pitches = pitches.split()
        if not isinstance(pitches, collections.abc.Iterable):
            pitches = [pitches]
        if isinstance(durations, (numbers.Number, tuple)):
            durations = [durations]
        nonreduced_fractions = Sequence(
            [mathtools.NonreducedFraction(_) for _ in durations]
        )
        size = max(len(nonreduced_fractions), len(pitches))
        nonreduced_fractions = nonreduced_fractions.repeat_to_length(size)
        pitches = Sequence(pitches).repeat_to_length(size)
        durations = Duration._group_by_implied_prolation(nonreduced_fractions)
        result: typing.List[typing.Union[Note, Tuplet]] = []
        for duration in durations:
            # get factors in denominator of duration group duration not 1 or 2
            factors = set(mathtools.factors(duration[0].denominator))
            factors.discard(1)
            factors.discard(2)
            ps = pitches[0 : len(duration)]
            pitches = pitches[len(duration) :]
            if len(factors) == 0:
                result.extend(
                    self._make_unprolated_notes(
                        ps,
                        duration,
                        increase_monotonic=self.increase_monotonic,
                        tag=self.tag,
                    )
                )
            else:
                # compute prolation
                denominator = duration[0].denominator
                numerator = mathtools.greatest_power_of_two_less_equal(denominator)
                multiplier = Multiplier(numerator, denominator)
                ratio = multiplier.reciprocal
                duration = [ratio * Duration(d) for d in duration]
                ns = self._make_unprolated_notes(
                    ps,
                    duration,
                    increase_monotonic=self.increase_monotonic,
                    tag=self.tag,
                )
                tuplet = Tuplet(multiplier, ns)
                result.append(tuplet)
        return Selection(result)

    ### PRIVATE METHODS ###

    @staticmethod
    def _make_unprolated_notes(pitches, durations, increase_monotonic=None, tag=None):
        assert len(pitches) == len(durations)
        result = []
        for pitch, duration in zip(pitches, durations):
            result.extend(
                LeafMaker._make_tied_leaf(
                    Note,
                    duration,
                    pitches=pitch,
                    increase_monotonic=increase_monotonic,
                    tag=tag,
                )
            )
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def increase_monotonic(self) -> typing.Optional[bool]:
        """
        Is true when durations increase monotonically.
        """
        return self._increase_monotonic

    @property
    def tag(self) -> typing.Optional[Tag]:
        r"""
        Gets tag.

        ..  container:: example

            >>> maker = abjad.NoteMaker(tag=abjad.Tag('note_maker'))
            >>> notes = maker([0], [(1, 16), (1, 8), (1, 8)])
            >>> staff = abjad.Staff(notes)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'16 %! note_maker
                    c'8 %! note_maker
                    c'8 %! note_maker
                }

        """
        return self._tag
