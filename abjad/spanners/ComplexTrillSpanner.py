import typing
from abjad.markup.Markup import Markup
from abjad.lilypondnames.LilyPondGrobOverride import \
    LilyPondGrobOverride
from abjad.pitch.NamedInterval import NamedInterval
from abjad.core.MultimeasureRest import MultimeasureRest
from abjad.core.Chord import Chord
from abjad.core.Note import Note
from abjad.core.Rest import Rest
from abjad.core.Skip import Skip
from abjad.top.inspect import inspect
from .Spanner import Spanner


class ComplexTrillSpanner(Spanner):
    r"""
    Complex trill spanner.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 ~ c'8 d'8 r8 e'8 ~ e'8 r8")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                ~
                c'8
                d'8
                r8
                e'8
                ~
                e'8
                r8
            }

        >>> complex_trill = abjad.ComplexTrillSpanner(
        ...     interval='P4',
        ...     )
        >>> abjad.attach(complex_trill, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \pitchedTrill
                c'4
                ~
                \startTrillSpan f'
                c'8
                <> \stopTrillSpan
                \pitchedTrill
                d'8
                - \tweak bound-details.left.text ##f
                \startTrillSpan g'
                <> \stopTrillSpan
                r8
                \pitchedTrill
                e'8
                ~
                \startTrillSpan a'
                e'8
                <> \stopTrillSpan
                r8
            }

    Allows for specifying a trill pitch via a named interval.

    Avoids silences.

    Restarts the trill on every new pitched logical tie.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_interval',
        )

    _start_command = r'\startTrillSpan'

    _stop_command = r'\stopTrillSpan'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        interval: str = None,
        ) -> None:
        Spanner.__init__(self)
        interval_ = None
        if interval is not None:
            interval_ = NamedInterval(interval)
        self._interval = interval_

    ### PRIVATE METHODS ###

    def _copy_keywords(self, new):
        new._interval = self.interval

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        prototype = (
            Rest,
            MultimeasureRest,
            Skip,
            )
        if isinstance(leaf, prototype):
            return bundle
        logical_tie = inspect(leaf).get_logical_tie()
        if leaf is logical_tie.head:
            previous_leaf = leaf._get_leaf(-1)
            if (previous_leaf is not None and
                not isinstance(previous_leaf, prototype) and
                inspect(previous_leaf).get_spanners(type(self))):
                override = LilyPondGrobOverride(
                    grob_name='TrillSpanner',
                    property_path=(
                        'bound-details',
                        'left',
                        'text',
                        ),
                    value=False,
                    )
                string = override.tweak_string()
                bundle.right.trill_pitches.append(string)
            if self.interval is not None:
                string = r'\pitchedTrill'
                bundle.opening.spanners.append(string)
                if isinstance(leaf, Note):
                    written_pitch = leaf.written_pitch
                elif isinstance(leaf, Chord):
                    if 0 < self.interval.semitones:
                        written_pitch = max(leaf.written_pitches)
                    elif self.interval.semitones < 0:
                        written_pitch = min(leaf.written_pitches)
                trill_pitch = written_pitch.transpose(self.interval)
                strings = self.start_command()
                strings[-1] = rf'{strings[-1]} {trill_pitch!s}'
            else:
                strings = self.start_command()
            bundle.right.trill_pitches.extend(strings)
        if leaf is logical_tie.tail:
            next_leaf = leaf._get_leaf(1)
            if next_leaf is not None:
                string = rf'<> {self.stop_command()}'
                bundle.after.commands.append(string)
            else:
                string = self.stop_command()
                bundle.right.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def interval(self) -> typing.Optional[NamedInterval]:
        r"""
        Gets optional interval of trill spanner.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> interval = abjad.NamedInterval('m3')
            >>> complex_trill = abjad.ComplexTrillSpanner(interval=interval)
            >>> abjad.attach(complex_trill, staff[1:-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \pitchedTrill
                    d'4
                    \startTrillSpan f'
                    <> \stopTrillSpan
                    \pitchedTrill
                    e'4
                    - \tweak bound-details.left.text ##f
                    \startTrillSpan g'
                    <> \stopTrillSpan
                    f'4
                }

            >>> complex_trill.interval
            NamedInterval('+m3')

        """
        return self._interval

    ### PUBLIC METHODS ###

    def start_command(self) -> typing.List[str]:
        r"""
        Gets start command.

        ..  container:: example

            >>> abjad.ComplexTrillSpanner().start_command()
            ['\\startTrillSpan']

        """
        return super(ComplexTrillSpanner, self).start_command()

    def stop_command(self) -> typing.Optional[str]:
        r"""
        Gets stop command.

        ..  container:: example

            >>> abjad.ComplexTrillSpanner().stop_command()
            '\\stopTrillSpan'

        """
        return super(ComplexTrillSpanner, self).stop_command()
