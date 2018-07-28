import typing
from abjad import enums
from abjad import typings
from abjad.core.Chord import Chord
from abjad.core.Component import Component
from abjad.core.MultimeasureRest import MultimeasureRest
from abjad.core.Note import Note
from abjad.core.Rest import Rest
from abjad.core.Skip import Skip
from abjad.indicators.Clef import Clef
from abjad.top.detach import detach
from abjad.top.inspect import inspect
from abjad.top.iterate import iterate
from abjad.top.sequence import sequence
from abjad.top.tweak import tweak
from abjad.utilities.Duration import Duration
from abjad.utilities.DurationInequality import DurationInequality
from abjad.utilities.String import String
from .Spanner import Spanner


class Tie(Spanner):
    r"""
    Tie.

    ..  container:: example

        Ties four notes:

        >>> staff = abjad.Staff("c'4 c' c' c'")
        >>> abjad.attach(abjad.Tie(), staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                ~
                c'4
                ~
                c'4
                ~
                c'4
            }

    ..  container:: example

        Removes any existing ties before attaching new tie:

        >>> staff = abjad.Staff("c'4 ~ c' ~ c' ~ c'")
        >>> abjad.attach(abjad.Tie(), staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                ~
                c'4
                ~
                c'4
                ~
                c'4
            }

    ..  container:: example

        Ties consecutive chords if all adjacent pairs have at least one pitch
        in common:

        >>> staff = abjad.Staff("<c'>4 <c' d'>4 <d'>4")
        >>> abjad.attach(abjad.Tie(), staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                <c'>4
                ~
                <c' d'>4
                ~
                <d'>4
            }

    ..  container:: example

        Enharmonics are allowed:

        >>> staff = abjad.Staff("c'4 bs c' dff'")
        >>> abjad.attach(abjad.Tie(), staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                ~
                bs4
                ~
                c'4
                ~
                dff'4
            }

    ..  container:: example

        Raises exception when pitches do not equal each other:

        >>> staff = abjad.Staff("c'4 d' e'8 ~ e'8 r4")
        >>> abjad.attach(abjad.Tie(), staff[:2])
        Traceback (most recent call last):
            ...
        Exception: Tie()._attachment_test_all():
          Pitch {0} does not equal pitch {2}.

        Raises exception on nonnote, nonchord leaves:

        >>> staff = abjad.Staff("c'4 d' e'8 ~ e'8 r4")
        >>> abjad.attach(abjad.Tie(), staff[-2:])
        Traceback (most recent call last):
            ...
        Exception: Tie()._attachment_test_all():
          Can only tie notes and chords.
          Not Rest('r4').

        Detaches existing ties before attach:

        >>> staff = abjad.Staff("c'4 d' e'8 ~ e'8 r4")
        >>> abjad.attach(abjad.Tie(), staff[2:4])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                d'4
                e'8
                ~
                e'8
                r4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        '_left_broken',
        '_repeat',
        '_right_broken',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: typing.Union[str, enums.VerticalAlignment] = None,
        left_broken: bool = None,
        repeat: typing.Union[
            bool,
            typings.IntegerPair,
            DurationInequality,
            ] = None,
        right_broken: bool = None,
        ) -> None:
        Spanner.__init__(self)
        direction = String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction
        if left_broken is not None:
            left_broken = bool(left_broken)
        self._left_broken = left_broken
        repeat_ = repeat
        repeat_ = self._coerce_inequality(repeat)
        if repeat_ is not None:
            assert isinstance(repeat_, (bool, DurationInequality))
        self._repeat = repeat_
        if right_broken is not None:
            right_broken = bool(right_broken)
        self._right_broken = right_broken

    ### PRIVATE METHODS ###

    def _add_tweaks_and_direction(self, command):
        strings = []
        contributions = tweak(self)._list_format_contributions()
        strings.extend(contributions)
        string = self._add_direction(command)
        strings.append(string)
        return strings

    def _attachment_test(self, component):
        if self._ignore_attachment_test:
            return True
        if not isinstance(component, (Chord, Note)):
            return False
        if inspect(component).has_spanner(Tie):
            return False
        return True

    def _attachment_test_all(self, component_expression):
        if self._ignore_attachment_test:
            return True
        written_pitches = []
        if isinstance(component_expression, Component):
            component_expression = [component_expression]
        for component in component_expression:
            if isinstance(component, Note):
                written_pitches.append(set([component.written_pitch.number]))
            elif isinstance(component, Chord):
                numbers = [_.number for _ in component.written_pitches]
                written_pitches.append(set(numbers))
            else:
                return [
                    'Can only tie notes and chords.',
                    f'Not {component!r}.',
                    ]
        for pair in sequence(written_pitches).nwise():
            if not set.intersection(*pair):
                return [f'Pitch {pair[0]} does not equal pitch {pair[1]}.']
        return True

    def _before_attach(self, argument):
        if self._ignore_before_attach:
            return
        for leaf in iterate(argument).leaves():
            detach(Tie, leaf)

    def _can_have_conventional_tie(self, leaf):
        if self.repeat is True:
            return False
        if self.repeat in (False, None):
            return True
        assert isinstance(self.repeat, DurationInequality)
        return not self.repeat(leaf)

    def _can_have_repeat_tie(self, leaf):
        if self.repeat is None:
            return False
        if isinstance(self.repeat, bool):
            return self.repeat
        previous = inspect(leaf).leaf(-1)
        if previous is None:
            return True
        if previous not in self:
            return False
        assert isinstance(self.repeat, DurationInequality)
        return self.repeat(previous)

    @staticmethod
    def _coerce_inequality(argument):
        if isinstance(argument, tuple) and len(argument) == 2:
            return DurationInequality(
                operator_string='>=',
                duration=argument,
                )
        return argument

    def _conventional_tie_strings(self):
        return self._add_tweaks_and_direction('~')

    def _copy_keywords(self, new):
        new._direction = self.direction
        new._repeat = self.repeat

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        prototype = (
            MultimeasureRest,
            Rest,
            Skip,
            )
        if isinstance(leaf, prototype):
            return bundle
        if self._can_have_repeat_tie(leaf):
            if leaf is self[0]:
                if self._left_broken:
                    strings = self._repeat_tie_strings(leaf)
                    strings = self._tag_show(strings)
                    bundle.after.spanners.extend(strings)
            else:
                strings = self._repeat_tie_strings(leaf)
                bundle.after.spanners.extend(strings)
        if self._can_have_conventional_tie(leaf):
            if leaf is self[-1]:
                if self._right_broken:
                    strings = self._conventional_tie_strings()
                    strings = self._tag_show(strings)
                    bundle.after.spanners.extend(strings)
            elif isinstance(leaf._get_leaf(1), prototype):
                pass
            else:
                strings = self._conventional_tie_strings()
                bundle.after.spanners.extend(strings)
        return bundle

    def _repeat_tie_strings(self, leaf):
        strings = []
        if self._should_force_repeat_tie_up(leaf):
            strings.append(r'- \tweak direction #up')
        strings_ = self._add_tweaks_and_direction(r'\repeatTie')
        strings.extend(strings_)
        return strings

    @staticmethod
    def _should_force_repeat_tie_up(leaf):
        if not isinstance(leaf, (Note, Chord)):
            return False
        if leaf.written_duration < Duration(1):
            return False
        clef = inspect(leaf).effective(Clef, default=Clef('treble'))
        if isinstance(leaf, Note):
            written_pitches = [leaf.written_pitch]
        else:
            written_pitches = leaf.written_pitches
        for written_pitch in written_pitches:
            staff_position = written_pitch.to_staff_position(clef=clef)
            if staff_position.number == 0:
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def cross_segment_examples(self):
        r"""
        Cross-segment examples.

        ..  container:: example

            [Tie] cross-segment example #1 (one-to-one):

            >>> segment_1 = abjad.Voice("c'4 d' f' f'", name='MainVoice')
            >>> tie = abjad.Tie(right_broken=True)
            >>> abjad.attach(tie, segment_1[-1:])
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    d'4
                    f'4
                    f'4
                %@% ~                                             %! SHOW_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("f'4 f' d' c'", name='MainVoice')
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    f'4
                    f'4
                    d'4
                    c'4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        d'4
                        f'4
                        f'4
                        ~                                         %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                    }
                    \context Voice = "MainVoice"
                    {
                        f'4
                        f'4
                        d'4
                        c'4
                    }
                }

        ..  container:: example

            [Tie] cross-segment example #2 (one-to-many):

            >>> segment_1 = abjad.Voice("c'4 d' f' f'", name='MainVoice')
            >>> tie = abjad.Tie(right_broken=True)
            >>> abjad.attach(tie, segment_1[-1:])
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    d'4
                    f'4
                    f'4
                %@% ~                                             %! SHOW_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("f'4 f' d' c'", name='MainVoice')
            >>> abjad.attach(abjad.Tie(), segment_2[:2])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    f'4
                    ~
                    f'4
                    d'4
                    c'4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        d'4
                        f'4
                        f'4
                        ~                                         %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                    }
                    \context Voice = "MainVoice"
                    {
                        f'4
                        ~
                        f'4
                        d'4
                        c'4
                    }
                }

        ..  container:: example

            [Tie] cross-segment example #3 (many-to-one):

            >>> segment_1 = abjad.Voice("c'4 d' f' f'", name='MainVoice')
            >>> tie = abjad.Tie(right_broken=True)
            >>> abjad.attach(tie, segment_1[-2:])
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    d'4
                    f'4
                    ~
                    f'4
                %@% ~                                             %! SHOW_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("f'4 f' d' c'", name='MainVoice')
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    f'4
                    f'4
                    d'4
                    c'4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        d'4
                        f'4
                        ~
                        f'4
                        ~                                         %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                    }
                    \context Voice = "MainVoice"
                    {
                        f'4
                        f'4
                        d'4
                        c'4
                    }
                }

        ..  container:: example

            [Tie] cross-segment example #4 (many-to-many):

            >>> segment_1 = abjad.Voice("c'4 d' f' f'", name='MainVoice')
            >>> tie = abjad.Tie(right_broken=True)
            >>> abjad.attach(tie, segment_1[-2:])
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    d'4
                    f'4
                    ~
                    f'4
                %@% ~                                             %! SHOW_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("f'4 f' d' c'", name='MainVoice')
            >>> abjad.attach(abjad.Tie(), segment_2[:2])

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    f'4
                    ~
                    f'4
                    d'4
                    c'4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        d'4
                        f'4
                        ~
                        f'4
                        ~                                         %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                    }
                    \context Voice = "MainVoice"
                    {
                        f'4
                        ~
                        f'4
                        d'4
                        c'4
                    }
                }

        ..  container:: example

            [Repeat tie] cross-segment example #1 (one-to-one):

            >>> segment_1 = abjad.Voice("c'4 d' f' f'", name='MainVoice')
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    d'4
                    f'4
                    f'4
                }

            >>> segment_2 = abjad.Voice("f'4 f' d' c'", name='MainVoice')
            >>> repeat_tie = abjad.Tie(repeat=True, left_broken=True)
            >>> abjad.attach(repeat_tie, segment_2[:1])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    f'4
                %@% \repeatTie                                    %! SHOW_TO_JOIN_BROKEN_SPANNERS
                    f'4
                    d'4
                    c'4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        d'4
                        f'4
                        f'4
                    }
                    \context Voice = "MainVoice"
                    {
                        f'4
                        \repeatTie                                %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                        f'4
                        d'4
                        c'4
                    }
                }

        ..  container:: example

            [Repeat tie] cross-segment example #2 (one-to-many):

            >>> segment_1 = abjad.Voice("c'4 d' f' f'", name='MainVoice')
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    d'4
                    f'4
                    f'4
                }

            >>> segment_2 = abjad.Voice("f'4 f' d' c'", name='MainVoice')
            >>> repeat_tie = abjad.Tie(left_broken=True, repeat=True)
            >>> abjad.attach(repeat_tie, segment_2[:2])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    f'4
                %@% \repeatTie                                    %! SHOW_TO_JOIN_BROKEN_SPANNERS
                    f'4
                    \repeatTie
                    d'4
                    c'4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        d'4
                        f'4
                        f'4
                    }
                    \context Voice = "MainVoice"
                    {
                        f'4
                        \repeatTie                                %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                        f'4
                        \repeatTie
                        d'4
                        c'4
                    }
                }

        ..  container:: example

            [Repeat tie] cross-segment example #3 (many-to-one):

            >>> segment_1 = abjad.Voice("c'4 d' f' f'", name='MainVoice')
            >>> repeat_tie = abjad.Tie(repeat=True)
            >>> abjad.attach(repeat_tie, segment_1[-2:])
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    d'4
                    f'4
                    f'4
                    \repeatTie
                }

            >>> segment_2 = abjad.Voice("f'4 f' d' c'", name='MainVoice')
            >>> repeat_tie = abjad.Tie(left_broken=True, repeat=True)
            >>> abjad.attach(repeat_tie, segment_2[:1])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    f'4
                %@% \repeatTie                                    %! SHOW_TO_JOIN_BROKEN_SPANNERS
                    f'4
                    d'4
                    c'4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        d'4
                        f'4
                        f'4
                        \repeatTie
                    }
                    \context Voice = "MainVoice"
                    {
                        f'4
                        \repeatTie                                %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                        f'4
                        d'4
                        c'4
                    }
                }

        ..  container:: example

            [Repeat tie] cross-segment example #4 (many-to-many):

            >>> segment_1 = abjad.Voice("c'4 d' f' f'", name='MainVoice')
            >>> repeat_tie = abjad.Tie(repeat=True)
            >>> abjad.attach(repeat_tie, segment_1[-2:])
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    d'4
                    f'4
                    f'4
                    \repeatTie
                }

            >>> segment_2 = abjad.Voice("f'4 f' d' c'", name='MainVoice')
            >>> repeat_tie = abjad.Tie(left_broken=True, repeat=True)
            >>> abjad.attach(repeat_tie, segment_2[:2])

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    f'4
                %@% \repeatTie                                    %! SHOW_TO_JOIN_BROKEN_SPANNERS
                    f'4
                    \repeatTie
                    d'4
                    c'4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        d'4
                        f'4
                        f'4
                        \repeatTie
                    }
                    \context Voice = "MainVoice"
                    {
                        f'4
                        \repeatTie                                %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                        f'4
                        \repeatTie
                        d'4
                        c'4
                    }
                }

        """
        pass

    @property
    def direction(self) -> typing.Optional[String]:
        r"""
        Gets direction.

        ..  container:: example

            Forces ties up:

            >>> staff = abjad.Staff("c'8 c'8 c'8 c'8")
            >>> tie = abjad.Tie(direction=abjad.Up)
            >>> abjad.attach(tie, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    ^ ~
                    c'8
                    ^ ~
                    c'8
                    ^ ~
                    c'8
                }

            >>> tie.direction
            '^'

        ..  container:: example

            Forces ties down:

            >>> staff = abjad.Staff("c'8 c'8 c'8 c'8")
            >>> tie = abjad.Tie(direction=abjad.Down)
            >>> abjad.attach(tie, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    _ ~
                    c'8
                    _ ~
                    c'8
                    _ ~
                    c'8
                }

            >>> tie.direction
            '_'

        ..  container:: example

            Positions ties according to LilyPond defaults:

            >>> staff = abjad.Staff("c'8 c'8 c'8 c'8")
            >>> tie = abjad.Tie(direction=None)
            >>> abjad.attach(tie, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    ~
                    c'8
                    ~
                    c'8
                    ~
                    c'8
                }

            >>> tie.direction is None
            True

        """
        return self._direction

    @property
    def left_broken(self) -> typing.Optional[bool]:
        """
        Is true when spanner is left-broken.
        """
        return self._left_broken

    @property
    def repeat(self) -> typing.Union[
        bool, DurationInequality, typings.IntegerPair, None,
        ]:
        r"""
        Gets repeat-tie threshold.

        ..  container:: example

            Formats all ties as repeat-ties when ``repeat`` is true:

            >>> staff = abjad.Staff("c'2 c'8 c'4.")
            >>> tie = abjad.Tie(repeat=True)
            >>> abjad.attach(tie, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'2
                    c'8
                    \repeatTie
                    c'4.
                    \repeatTie
                }

        ..  container:: example

            Formats only ties that satisfy duration inequality when ``repeat``
            is a duration inequality:

            >>> staff = abjad.Staff("c'2 c'8 c'4.")
            >>> repeat = abjad.DurationInequality(
            ...     operator_string='>=',
            ...     duration=abjad.Duration(1, 4),
            ...     )
            >>> tie = abjad.Tie(repeat=repeat)
            >>> abjad.attach(tie, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..   docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'2
                    c'8
                    \repeatTie
                    ~
                    c'4.
                }

            Coerces integer pair to >= inequality:

            >>> staff = abjad.Staff("c'2 c'8 c'4.")
            >>> tie = abjad.Tie(repeat=(1, 4))
            >>> abjad.attach(tie, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..   docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'2
                    c'8
                    \repeatTie
                    ~
                    c'4.
                }

            Durations that satisfy inequality can be said to "meet repeat-tie
            threshold." Durations that do not meet repeat-tie threshold format
            conventional tie on current note; durations that do meet repeat-tie
            threshold format repeat-tie on following note.

        ..  container:: example

            LILYPOND FIX. Automatically tweaks repeat tie direction up when
            repeat tie connects to long-duration note at staff position zero:

            >>> tie = abjad.Tie(repeat=True)
            >>> staff = abjad.Staff(r"b'4 b'4 b'2 b'1 b'\breve")
            >>> abjad.attach(abjad.TimeSignature((8, 4)), staff[-1])
            >>> abjad.attach(tie, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..   docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    b'4
                    b'4
                    \repeatTie
                    b'2
                    \repeatTie
                    b'1
                    - \tweak direction #up
                    \repeatTie
                    \time 8/4
                    b'\breve
                    - \tweak direction #up
                    \repeatTie
                }

            Without this fix, LilyPond incorrectly down-renders the last two
            repeat-ties in the example above.

        """
        return self._repeat

    @property
    def right_broken(self) -> typing.Optional[bool]:
        """
        Is true when spanner is right-broken.
        """
        return self._right_broken
