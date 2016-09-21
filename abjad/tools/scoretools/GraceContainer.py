# -*- coding: utf-8 -*-
from abjad.tools.scoretools.Container import Container


class GraceContainer(Container):
    r'''A grace container.

    .. container:: example

        **Example 1.** Grace notes:

        ::

            >>> voice = Voice("c'4 d'4 e'4 f'4")
            >>> grace_notes = [Note("c'16"), Note("d'16")]
            >>> grace_container = scoretools.GraceContainer(
            ...     grace_notes,
            ...     kind='grace',
            ...     )
            >>> attach(grace_container, voice[1])
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'4
                \grace {
                    c'16
                    d'16
                }
                d'4
                e'4
                f'4
            }

    ..  container:: example

        **Example 2.** After-grace notes:

        ::

            >>> voice = Voice("c'4 d'4 e'4 f'4")
            >>> grace_notes = [Note("c'16"), Note("d'16")]
            >>> grace_container = scoretools.GraceContainer(
            ...     grace_notes,
            ...     kind='after',
            ...     )
            >>> attach(grace_container, voice[1])
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'4
                \afterGrace
                d'4
                {
                    c'16
                    d'16
                }
                e'4
                f'4
            }

    Fill grace containers with notes, rests or chords.

    Attach grace containers to notes, rests or chords.

    ..  container:: example

        **Example 3.** Detaches all grace containers:

        ::

            >>> voice = Voice("c'4 d'4 e'4 f'4")
            >>> note = Note("cs'16")
            >>> grace_container = scoretools.GraceContainer(
            ...     [note],
            ...     kind='grace',
            ...     )
            >>> attach(grace_container, voice[1])
            >>> note = Note("ds'16")
            >>> after_grace_container = scoretools.GraceContainer(
            ...     [note],
            ...     kind='after',
            ...     )
            >>> attach(after_grace_container, voice[1])
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'4
                \grace {
                    cs'16
                }
                \afterGrace
                d'4
                {
                    ds'16
                }
                e'4
                f'4
            }

        ::

            >>> detach(scoretools.GraceContainer, voice[1])
            (GraceContainer(), GraceContainer())
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'4
                d'4
                e'4
                f'4
            }

    ..  container:: example

        **Example 4.** Detaches (proper) grace container but leaves after grace
        container attached:

        ::

            >>> voice = Voice("c'4 d'4 e'4 f'4")
            >>> note = Note("cs'16")
            >>> grace_container = scoretools.GraceContainer(
            ...     [note],
            ...     kind='grace',
            ...     )
            >>> attach(grace_container, voice[1])
            >>> note = Note("ds'16")
            >>> after_grace_container = scoretools.GraceContainer(
            ...     [note],
            ...     kind='after',
            ...     )
            >>> attach(after_grace_container, voice[1])
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'4
                \grace {
                    cs'16
                }
                \afterGrace
                d'4
                {
                    ds'16
                }
                e'4
                f'4
            }

        ::

            >>> detach(grace_container, voice[1])
            (GraceContainer(),)
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'4
                \afterGrace
                d'4
                {
                    ds'16
                }
                e'4
                f'4
            }

    ..  container:: example

        **Example 5.** Detaches after grace container but leaves (proper) grace
        container attached:

        ::

            >>> voice = Voice("c'4 d'4 e'4 f'4")
            >>> note = Note("cs'16")
            >>> grace_container = scoretools.GraceContainer(
            ...     [note],
            ...     kind='grace',
            ...     )
            >>> attach(grace_container, voice[1])
            >>> note = Note("ds'16")
            >>> after_grace_container = scoretools.GraceContainer(
            ...     [note],
            ...     kind='after',
            ...     )
            >>> attach(after_grace_container, voice[1])
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'4
                \grace {
                    cs'16
                }
                \afterGrace
                d'4
                {
                    ds'16
                }
                e'4
                f'4
            }

        ::

            >>> detach(after_grace_container, voice[1])
            (GraceContainer(),)
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'4
                \grace {
                    cs'16
                }
                d'4
                e'4
                f'4
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = (
        '_carrier',
        '_kind',
        )

    _allowable_kinds = (
        'after',
        'grace',
        'acciaccatura',
        'appoggiatura',
        )

    ### INITIALIZER ###

    def __init__(self, music=None, kind='grace'):
        # self._carrier is a reference to the leaf carrying grace music
        self._carrier = None
        Container.__init__(self, music)
        self.kind = kind

    ### PRIVATE METHODS ###

    def _attach(self, leaf):
        from abjad.tools import scoretools
        if not isinstance(leaf, scoretools.Leaf):
            message = 'must attach to leaf: {!r}.'
            message = message.format(leaf)
            raise TypeError(message)
        if self.kind == 'after':
            leaf._after_grace = self
        else:
            leaf._grace = self
        self._carrier = leaf

    def _copy_with_indicators_but_without_children_or_spanners(self):
        new = Container._copy_with_indicators_but_without_children_or_spanners(
            self)
        new.kind = self.kind
        return new

    def _detach(self):
        if self._carrier is not None:
            carrier = self._carrier
            if self.kind == 'after':
                carrier._after_grace = None
            else:
                carrier._grace = None
            self._carrier = None
            self[:] = []
        return self

    def _format_open_brackets_slot(self, bundle):
        result = []
        kind = self.kind
        if kind == 'after':
            result.append([('grace_brackets', 'open'), ['{']])
        else:
            contributor = ('grace_brackets', 'open')
            contributions = [r'\{} {{'.format(kind)]
            result.append([contributor, contributions])
        return tuple(result)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()

    ### PUBLIC PROPERTIES ###

    @property
    def kind(self):
        r'''Gets and sets `kind`.

        .. container:: example

            **Example 1.** Grace notes:

            ::

                >>> voice = Voice("c'4 d'4 e'4 f'4")
                >>> grace_container = scoretools.GraceContainer(
                ...     [Note("e'16")],
                ...     kind='grace',
                ...     )
                >>> attach(grace_container, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'4
                    \grace {
                        e'16
                    }
                    d'4
                    e'4
                    f'4
                }

            LilyPond positions grace notes immediately before main notes.

            LilyPond formats grace notes with neither a slashed nor a slur.

        .. container:: example

            **Example 2.** Acciaccatura:

            ::

                >>> voice = Voice("c'4 d'4 e'4 f'4")
                >>> grace_container = scoretools.GraceContainer(
                ...     [Note("e'16")],
                ...     kind='acciaccatura',
                ...     )
                >>> attach(grace_container, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'4
                    \acciaccatura {
                        e'16
                    }
                    d'4
                    e'4
                    f'4
                }

            Acciaccaturas are played before the beat.

            LilyPond positions acciaccaturas immediately before main notes.

            LilyPond formats one-note acciaccaturas with a slashed stem and a
            slur.

            ..  note:: LilyPond fails to format multinote acciaccaturas
                with a slashed stem. This means that multinote
                acciaccaturas look exactly like appoggiaturas.

        .. container:: example

            **Example 3.** Appoggiatura:

            ::

                >>> voice = Voice("c'4 d'4 e'4 f'4")
                >>> grace_container = scoretools.GraceContainer(
                ...     [Note("e'16")],
                ...     kind='appoggiatura',
                ...     )
                >>> attach(grace_container, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'4
                    \appoggiatura {
                        e'16
                    }
                    d'4
                    e'4
                    f'4
                }

            Appoggiaturas are played on the beat.

            LilyPond positions appoggiaturas immediately before main notes.

            LilyPond formats appoggiaturas with a slur but without a slashed
            stem.

        .. container:: example

            **Example 4.** After-grace notes:

            ::

                >>> voice = Voice("c'4 d'4 e'4 f'4")
                >>> string = '#(define afterGraceFraction (cons 15 16))'
                >>> command = indicatortools.LilyPondCommand(string)
                >>> attach(command, voice[0])
                >>> grace_container = scoretools.GraceContainer(
                ...     [Note("g'16")],
                ...     kind='after',
                ...     )
                >>> attach(grace_container, voice[-1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    #(define afterGraceFraction (cons 15 16))
                    c'4
                    d'4
                    e'4
                    \afterGrace
                    f'4
                    {
                        g'16
                    }
                }

            After-grace notes are played at the very end of the note they
            follow.

            Use after-grace notes when you need to end a piece of music with
            grace notes.

            LilyPond positions after-grace notes at a point 3/4 of the way
            after the note they follow. The resulting spacing is usually too
            loose.

            Customize aftterGraceFraction as shown above.

        Defaults to ``'grace'``.

        Set to ``'grace'``, ``'acciaccatura'``, ``'appoggiatura'`` or
        ``'after'``.

        Returns ``'grace'``, ``'acciaccatura'``, ``'appoggiatura'`` or
        ``'after'``.
        '''
        return self._kind

    @kind.setter
    def kind(self, arg):
        if arg not in self._allowable_kinds:
            message = 'unknown grace container kind: {!r}.'
            message = message.format(arg)
            raise Exception(message)
        self._kind = arg
