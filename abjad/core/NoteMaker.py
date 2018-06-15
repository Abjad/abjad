import collections
import numbers
import typing
from abjad.system.AbjadValueObject import AbjadValueObject


class NoteMaker(AbjadValueObject):
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

        Set ``decrease_monotonic=True`` to express tied values in decreasing
        duration:

        >>> maker = abjad.NoteMaker(decrease_monotonic=True)
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

        Set ``decrease_monotonic=False`` to express tied values in increasing
        duration:

        >>> maker = abjad.NoteMaker(decrease_monotonic=False)
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

        Uses repeat ties:

        >>> maker = abjad.NoteMaker(repeat_ties=True)
        >>> notes = maker([0], [(13, 16)])
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'2.
                c'16
                \repeatTie
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

    __documentation_section__ = 'Makers'

    __slots__ = (
        '_decrease_monotonic',
        '_repeat_ties',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        decrease_monotonic=True,
        repeat_ties=False,
        ):
        self._decrease_monotonic = decrease_monotonic
        self._repeat_ties = repeat_ties

    ### SPECIAL METHODS ###

    def __call__(self, pitches, durations):
        """
        Calls note-maker on ``pitches`` and ``durations``.

        Returns selection.
        """
        import abjad
        if isinstance(pitches, str):
            pitches = pitches.split()
        if not isinstance(pitches, collections.Iterable):
            pitches = [pitches]
        if isinstance(durations, (numbers.Number, tuple)):
            durations = [durations]
        nonreduced_fractions = [abjad.NonreducedFraction(_) for _ in durations]
        size = max(len(nonreduced_fractions), len(pitches))
        nonreduced_fractions = abjad.sequence(nonreduced_fractions)
        nonreduced_fractions = nonreduced_fractions.repeat_to_length(size)
        pitches = abjad.sequence(pitches).repeat_to_length(size)
        Duration = abjad.Duration
        durations = Duration._group_by_implied_prolation(
            nonreduced_fractions)
        result = []
        for duration in durations:
            # get factors in denominator of duration group duration not 1 or 2
            factors = set(abjad.mathtools.factors(duration[0].denominator))
            factors.discard(1)
            factors.discard(2)
            ps = pitches[0:len(duration)]
            pitches = pitches[len(duration):]
            if len(factors) == 0:
                result.extend(
                    self._make_unprolated_notes(
                        ps,
                        duration,
                        decrease_monotonic=self.decrease_monotonic,
                        repeat_ties=self.repeat_ties,
                        )
                    )
            else:
                # compute prolation
                denominator = duration[0].denominator
                numerator = abjad.mathtools.greatest_power_of_two_less_equal(
                    denominator)
                multiplier = (numerator, denominator)
                ratio = 1 / abjad.Fraction(*multiplier)
                duration = [ratio * abjad.Duration(d) for d in duration]
                ns = self._make_unprolated_notes(
                    ps,
                    duration,
                    decrease_monotonic=self.decrease_monotonic,
                    repeat_ties=self.repeat_ties,
                    )
                tuplet = abjad.Tuplet(multiplier, ns)
                result.append(tuplet)
        result = abjad.select(result)
        return result

    ### PRIVATE METHODS ###

    @staticmethod
    def _make_unprolated_notes(
        pitches,
        durations,
        decrease_monotonic=True,
        repeat_ties=False,
        ):
        import abjad
        assert len(pitches) == len(durations)
        result = []
        for pitch, duration in zip(pitches, durations):
            result.extend(
                abjad.LeafMaker._make_tied_leaf(
                    abjad.Note,
                    duration,
                    pitches=pitch,
                    decrease_monotonic=decrease_monotonic,
                    repeat_ties=repeat_ties,
                    )
                )
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def decrease_monotonic(self):
        """
        Is true when durations decrease monotonically.

        Returns true, false or none.
        """
        return self._decrease_monotonic

    @property
    def repeat_ties(self) -> typing.Optional[bool]:
        """
        Is true when ties are repeat ties.
        """
        return self._repeat_ties
