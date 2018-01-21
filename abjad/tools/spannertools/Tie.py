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
            \new Staff {
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
            \new Staff {
                c'4 ~
                c'4 ~
                c'4 ~
                c'4
            }

    ..  container:: example

        Fails attachment test when pitches differ:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Tie(), staff[:])
        Traceback (most recent call last):
            ...
        Exception: Tie() attachment test fails for ...
        <BLANKLINE>
        Selection([Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")])

    ..  container:: example

        Ties consecutive chords if all adjacent pairs have at least one pitch
        in common:

        >>> staff = abjad.Staff("<c'>4 <c' d'>4 <d'>4")
        >>> abjad.attach(abjad.Tie(), staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                <c'>4 ~
                <c' d'>4 ~
                <d'>4
            }

    ..  container:: example

        Conventional ties can be right-open tagged (with strict formatting) for
        use at the end of a segment:

        >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
        >>> abjad.attach(abjad.Tie(), segment_1[-1:], right_open=True)
        >>> abjad.f(segment_1, strict=True)
        \context Voice = "MainVoice" {
            c'4
            d'4
            e'4
            f'4
        %@% ~     %! RIGHT_OPEN_TIE
        }

        >>> abjad.show(segment_1) # doctest: +SKIP

        >>> segment_2 = abjad.Voice("f'4 e' d' c'", name='MainVoice')
        >>> abjad.f(segment_2, strict=True)
        \context Voice = "MainVoice" {
            f'4
            e'4
            d'4
            c'4
        }

        >>> abjad.show(segment_2) # doctest: +SKIP

        >>> container = abjad.Container([segment_1, segment_2])
        >>> abjad.f(container, strict=True)
        {
            \context Voice = "MainVoice" {
                c'4
                d'4
                e'4
                f'4
            %@% ~     %! RIGHT_OPEN_TIE
            }
            \context Voice = "MainVoice" {
                f'4
                e'4
                d'4
                c'4
            }
        }

        >>> abjad.show(container) # doctest: +SKIP

        >>> text = format(container, 'lilypond:strict')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> text, count = abjad.activate(text, abjad.tags.RIGHT_OPEN_TIE)
        >>> print(text)
        {
            \context Voice = "MainVoice" {
                c'4
                d'4
                e'4
                f'4
                ~     %! RIGHT_OPEN_TIE %@%
            }
            \context Voice = "MainVoice" {
                f'4
                e'4
                d'4
                c'4
            }
        }

        >>> lines = text.split('\n')
        >>> lilypond_file = abjad.LilyPondFile.new(lines)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  container:: example

        Repeat ties can be left-open tagged (with strict formatting) for use at
        the beginning of a segment:

        >>> staff = abjad.Staff("c'4 c' c' c'")
        >>> tie = abjad.Tie(repeat=True)
        >>> abjad.attach(tie, staff[:], left_open=True)
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff, strict=True)
        \new Staff {
            c'4
        %@% \repeatTie     %! LEFT_OPEN_REPEAT_TIE
            c'4
            \repeatTie
            c'4
            \repeatTie
            c'4
            \repeatTie
        }

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
        repeat=None,
        ):
        import abjad
        Spanner.__init__(self, overrides=overrides)
        direction = abjad.String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction
        self._repeat = repeat

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
                written_pitches.append(set([component.written_pitch]))
            elif isinstance(component, abjad.Chord):
                written_pitches.append(set(component.written_pitches))
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
            if self._is_my_last_leaf(leaf):
                if not self._right_open:
                    return bundle
                elif self.direction is not None:
                    string = '{} ~'.format(self.direction)
                else:
                    string = '~'
                strings = abjad.LilyPondFormatManager.tag(
                    [string],
                    deactivate=True,
                    tag=abjad.tags.RIGHT_OPEN_TIE,
                    )
                assert len(strings) == 1
                string = strings[0]
                bundle.right.spanners.append(string)
            elif isinstance(leaf._get_leaf(1), silent):
                return bundle
            elif self.direction is not None:
                string = '{} ~'.format(self.direction)
                bundle.right.spanners.append(string)
            else:
                bundle.right.spanners.append('~')
        else:
            if self._is_my_first_leaf(leaf):
                if not self._left_open:
                    return bundle
                elif self.direction is not None:
                    string = r'{} \repeatTie'.format(self.direction)
                else:
                    string = r'\repeatTie'
                strings = abjad.LilyPondFormatManager.tag(
                    [string],
                    deactivate=True,
                    tag='LEFT_OPEN_REPEAT_TIE',
                    )
                assert len(strings) == 1
                string = strings[0]
                bundle.right.spanners.append(string)
            elif self.direction is not None:
                string = r'{} \repeatTie'.format(self.direction)
                bundle.right.spanners.append(string)
            else:
                bundle.right.spanners.append(r'\repeatTie')
        return bundle

    ### PUBLIC PROPERTIES ###

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
                \new Staff {
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
                \new Staff {
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
                \new Staff {
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
                \new Staff {
                    c'8
                    c'8 ^ \repeatTie
                    c'8 ^ \repeatTie
                    c'8 ^ \repeatTie
                }

        Returns true, false or none.
        '''
        return self._repeat
