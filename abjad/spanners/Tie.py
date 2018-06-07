import typing
from abjad.core.Chord import Chord
from abjad.core.Component import Component
from abjad.core.MultimeasureRest import MultimeasureRest
from abjad.core.Note import Note
from abjad.core.Rest import Rest
from abjad.core.Skip import Skip
from abjad.enumerations import VerticalAlignment
from abjad.top.detach import detach
from abjad.top.inspect import inspect
from abjad.top.iterate import iterate
from abjad.top.sequence import sequence
from abjad.top.tweak import tweak
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
        '_repeat',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: typing.Union[str, VerticalAlignment] = None,
        repeat: bool = None,
        ) -> None:
        Spanner.__init__(self)
        direction = String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction
        self._repeat = repeat

    ### PRIVATE METHODS ###

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

    def _copy_keywords(self, new):
        new._direction = self.direction
        new._repeat = self.repeat

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        silent = (
            MultimeasureRest,
            Rest,
            Skip,
            )
        if isinstance(leaf, silent):
            return bundle
        if not self.repeat:
            if leaf is self[-1]:
                if not self._right_broken:
                    return bundle
                strings = self.start_command()
                strings = self._tag_show(strings)
                bundle.right.spanners.extend(strings)
            elif isinstance(leaf._get_leaf(1), silent):
                return bundle
            else:
                strings = self.start_command()
                bundle.right.spanners.extend(strings)
        else:
            if leaf is self[0]:
                if not self._left_broken:
                    return bundle
                strings = [self.stop_command()]
                strings = self._tag_show(strings)
                bundle.right.spanners.extend(strings)
            else:
                strings = [self.stop_command()]
                bundle.right.spanners.extend(strings)
        return bundle

    ### PUBLIC PROPERTIES ###

    def cross_segment_examples(self):
        r"""
        Cross-segment examples.

        ..  container:: example

            [Tie] cross-segment example #1 (one-to-one):

            >>> segment_1 = abjad.Voice("c'4 d' f' f'", name='MainVoice')
            >>> abjad.attach(abjad.Tie(), segment_1[-1:], right_broken=True)
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
            >>> abjad.attach(abjad.Tie(), segment_1[-1:], right_broken=True)
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
            >>> abjad.attach(abjad.Tie(), segment_1[-2:], right_broken=True)
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
            >>> abjad.attach(abjad.Tie(), segment_1[-2:], right_broken=True)
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
            >>> repeat_tie = abjad.Tie(repeat=True)
            >>> abjad.attach(repeat_tie, segment_2[:1], left_broken=True)
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
            >>> repeat_tie = abjad.Tie(repeat=True)
            >>> abjad.attach(repeat_tie, segment_2[:2], left_broken=True)
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
            >>> repeat_tie = abjad.Tie(repeat=True)
            >>> abjad.attach(repeat_tie, segment_2[:1], left_broken=True)
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
            >>> repeat_tie = abjad.Tie(repeat=True)
            >>> abjad.attach(repeat_tie, segment_2[:2], left_broken=True)

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
    def repeat(self) -> typing.Optional[bool]:
        r"""
        Is true when tie should use the LilyPond ``\repeatTie`` command.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 c'8 c'8 c'8")
            >>> tie = abjad.Tie(direction=abjad.Up, repeat=True)
            >>> abjad.attach(tie, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    c'8
                    ^ \repeatTie
                    c'8
                    ^ \repeatTie
                    c'8
                    ^ \repeatTie
                }

        """
        return self._repeat

    ### PUBLIC METHODS ###

    def start_command(self) -> typing.List[str]:
        """
        Gets start command.

        ..  container:: example

            >>> abjad.Tie().start_command()
            ['~']

        ..  container:: example

            >>> abjad.Tie(repeat=True).start_command()
            []

        """
        strings: typing.List[str] = []
        if self.repeat:
            return strings
        contributions = tweak(self)._list_format_contributions()
        strings.extend(contributions)
        string = '~'
        string = self._add_direction(string)
        strings.append(string)
        return strings

    # TODO: teach stop_command to return list including tweaks
    def stop_command(self) -> typing.Optional[str]:
        r"""
        Gets stop command.

        ..  container:: example

            >>> abjad.Tie().stop_command()
            ''

        ..  container:: example

            >>> abjad.Tie(repeat=True).stop_command()
            '\\repeatTie'

        """
        if self.repeat:
            string = r'\repeatTie'
            string = self._add_direction(string)
            return string
        else:
            return ''
