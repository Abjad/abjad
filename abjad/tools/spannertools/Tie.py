from abjad.tools.datastructuretools.String import String
from .Spanner import Spanner


class Tie(Spanner):
    r'''Tie.

    ..  container:: example

        Ties four notes:

        >>> staff = abjad.Staff("c'4 c' c' c'")
        >>> abjad.attach(abjad.Tie(), staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4 ~
                c'4 ~
                c'4 ~
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
                c'4 ~
                c'4 ~
                c'4 ~
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
                <c'>4 ~
                <c' d'>4 ~
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
                c'4 ~
                bs4 ~
                c'4 ~
                dff'4
            }

    ..  container:: example

        Raises exception at attach-time when pitches differ:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Tie(), staff[:])
        Traceback (most recent call last):
            ...
        Exception: Tie() attachment test fails for ...
        <BLANKLINE>
        Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        '_repeat',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        direction=None,
        overrides=None,
        repeat: bool = None,
        ) -> None:
        Spanner.__init__(self, overrides=overrides)
        direction = String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction
        self._repeat: bool = repeat

    ### PRIVATE METHODS ###

    def _attachment_test(self, component):
        import abjad
        if self._ignore_attachment_test:
            return True
        if not isinstance(component, (abjad.Chord, abjad.Note)):
            return False
        if abjad.inspect(component).has_spanner(abjad.Tie):
            return False
        return True

    def _attachment_test_all(self, component_expression):
        import abjad
        if self._ignore_attachment_test:
            return True
        written_pitches = []
        if isinstance(component_expression, abjad.Component):
            component_expression = [component_expression]
        for component in component_expression:
            if isinstance(component, abjad.Note):
                written_pitches.append(set([component.written_pitch.number]))
            elif isinstance(component, abjad.Chord):
                numbers = [_.number for _ in component.written_pitches]
                written_pitches.append(set(numbers))
            else:
                return False
        for pair in abjad.sequence(written_pitches).nwise():
            if not set.intersection(*pair):
                return False
        for component in component_expression:
            if abjad.inspect(component).has_spanner(abjad.Tie):
                return False
        return True

    def _before_attach(self, argument):
        import abjad
        if self._ignore_before_attach:
            return
        for leaf in abjad.iterate(argument).leaves():
            abjad.detach(Tie, leaf)

    def _copy_keyword_args(self, new):
        new._direction = self.direction
        new._repeat = self.repeat

    def _get_lilypond_format_bundle(self, leaf):
        import abjad
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        silent = (
            abjad.MultimeasureRest,
            abjad.Rest,
            abjad.Skip,
            )
        if isinstance(leaf, silent):
            return bundle
        if not self.repeat:
            if leaf is self[-1]:
                if not self._right_broken:
                    return bundle
                elif self.direction is not None:
                    strings = ['{} ~'.format(self.direction)]
                else:
                    strings = ['~']
                strings = self._tag_show(strings)
                bundle.right.spanners.extend(strings)
            elif isinstance(leaf._get_leaf(1), silent):
                return bundle
            elif self.direction is not None:
                strings = ['{} ~'.format(self.direction)]
                bundle.right.spanners.extend(strings)
            else:
                strings = ['~']
                bundle.right.spanners.extend(strings)
        else:
            if leaf is self[0]:
                if not self._left_broken:
                    return bundle
                elif self.direction is not None:
                    strings = [r'{} \repeatTie'.format(self.direction)]
                else:
                    strings = [r'\repeatTie']
                strings = self._tag_show(strings)
                bundle.right.spanners.extend(strings)
            elif self.direction is not None:
                strings = [r'{} \repeatTie'.format(self.direction)]
                bundle.right.spanners.extend(strings)
            else:
                strings = [r'\repeatTie']
                bundle.right.spanners.extend(strings)
        return bundle

    ### PUBLIC PROPERTIES ###

    def cross_segment_examples(self):
        r'''Cross-segment examples.

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
            >>> text = format(container, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.broken_spanner_join_job(text)
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
            >>> text = format(container, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.broken_spanner_join_job(text)
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
            >>> text = format(container, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.broken_spanner_join_job(text)
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
            >>> text = format(container, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.broken_spanner_join_job(text)
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
            >>> text = format(container, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.broken_spanner_join_job(text)
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
            >>> text = format(container, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.broken_spanner_join_job(text)
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
            >>> text = format(container, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.broken_spanner_join_job(text)
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
            >>> text = format(container, 'lilypond:strict')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.broken_spanner_join_job(text)
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

        '''
        pass

    @property
    def direction(self):
        r'''Gets direction.

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
                    c'8 ^ ~
                    c'8 ^ ~
                    c'8 ^ ~
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
                    c'8 _ ~
                    c'8 _ ~
                    c'8 _ ~
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
                    c'8 ~
                    c'8 ~
                    c'8 ~
                    c'8
                }

            >>> tie.direction is None
            True

        Defaults to none.

        Set to up, down or none.

        Returns up, down or none.
        '''
        return self._direction

    @property
    def repeat(self):
        r'''Is true when tie should use the LilyPond ``\repeatTie`` command.

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
                    c'8 ^ \repeatTie
                    c'8 ^ \repeatTie
                    c'8 ^ \repeatTie
                }

        Returns true, false or none.
        '''
        return self._repeat
