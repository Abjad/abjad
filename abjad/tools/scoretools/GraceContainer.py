# -*- coding: utf-8 -*-
from abjad.tools.scoretools.Container import Container


class GraceContainer(Container):
    r'''A grace container.

    .. container:: example

        **Example 1.** Grace notes:

        ::

            >>> voice = Voice("c'4 d'4 e'4 f'4")
            >>> beam = spannertools.Beam()
            >>> attach(beam, voice[:])
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
                c'4 [
                \grace {
                    c'16
                    d'16
                }
                d'4
                e'4
                f'4 ]
            }

    ..  container:: example

        **Example 2.** After-grace notes:

        ::

            >>> voice = Voice("c'4 d'4 e'4 f'4")
            >>> beam = spannertools.Beam()
            >>> attach(beam, voice[:])
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
                c'4 [
                \afterGrace
                d'4
                {
                    c'16
                    d'16
                }
                e'4
                f'4 ]
            }

    Fill grace containers with notes, rests or chords.

    Attach grace containers to notes, rests or chords.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = (
        '_carrier',
        '_kind',
        )

    ### INITIALIZER ###

    def __init__(self, music=None, kind='grace'):
        # self._carrier is a reference to the leaf carrying grace music
        self._carrier = None
        Container.__init__(self, music)
        self.kind = kind

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()

    ### PRIVATE METHODS ###

    def _attach(self, arg):
        from abjad.tools import scoretools
        if not isinstance(arg, scoretools.Leaf):
            message = 'object to which grace container attaches'
            message += ' must be leaf: {!r}.'
            message = message.format(arg)
            raise TypeError(message)
        if self.kind == 'after':
            arg._after_grace = self
        else:
            arg._grace = self
        self._carrier = arg

    def _copy_with_indicators_but_without_children_or_spanners(self):
        new = Container._copy_with_indicators_but_without_children_or_spanners(self)
        new.kind = self.kind
        return new

    def _detach(self):
        if self._carrier is not None:
            carrier = self._carrier
            if self.kind == 'after':
                #delattr(carrier, '_after_grace')
                carrier._after_grace = None
            else:
                #delattr(carrier, '_grace')
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

    ### PUBLIC PROPERTIES ###

    @property
    def kind(self):
        r'''Gets and sets `kind`.

        .. container:: example

            **Example 1.** Grace notes:

            ::

                >>> voice = Voice("c'4 d'4 e'4 f'4")
                >>> beam = spannertools.Beam()
                >>> attach(beam, voice[:])
                >>> grace_notes = [Note("bf16"), Note("c'16")]
                >>> grace_container = scoretools.GraceContainer(
                ...     grace_notes,
                ...     kind='grace',
                ...     )
                >>> attach(grace_container, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'4 [
                    \grace {
                        bf16
                        c'16
                    }
                    d'4
                    e'4
                    f'4 ]
                }

        .. container:: example

            **Example 2.** After-grace notes:

            ::

                >>> voice = Voice("c'4 d'4 e'4 f'4")
                >>> beam = spannertools.Beam()
                >>> attach(beam, voice[:])
                >>> grace_notes = [Note("cs'16"), Note("d'16")]
                >>> grace_container = scoretools.GraceContainer(
                ...     grace_notes,
                ...     kind='after',
                ...     )
                >>> attach(grace_container, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'4 [
                    \afterGrace
                    d'4
                    {
                        cs'16
                        d'16
                    }
                    e'4
                    f'4 ]
                }

        .. container:: example

            **Example 3.** Acciaccatura:

            ::

                >>> voice = Voice("c'4 d'4 e'4 f'4")
                >>> beam = spannertools.Beam()
                >>> attach(beam, voice[:])
                >>> grace_notes = [Note("bf16"), Note("c'16")]
                >>> grace_container = scoretools.GraceContainer(
                ...     grace_notes,
                ...     kind='acciaccatura',
                ...     )
                >>> attach(grace_container, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'4 [
                    \acciaccatura {
                        bf16
                        c'16
                    }
                    d'4
                    e'4
                    f'4 ]
                }

        .. container:: example

            **Example 4.** Appoggiatura:

            ::

                >>> voice = Voice("c'4 d'4 e'4 f'4")
                >>> beam = spannertools.Beam()
                >>> attach(beam, voice[:])
                >>> grace_notes = [Note("bf16"), Note("c'16")]
                >>> grace_container = scoretools.GraceContainer(
                ...     grace_notes,
                ...     kind='appoggiatura',
                ...     )
                >>> attach(grace_container, voice[1])
                >>> show(voice) # doctest: +SKIP

            ..  doctest::

                >>> f(voice)
                \new Voice {
                    c'4 [
                    \appoggiatura {
                        bf16
                        c'16
                    }
                    d'4
                    e'4
                    f'4 ]
                }

        Defaults to ``'grace'``.

        Set to ``'grace'``, ``'after'``, ``'acciaccatura'`` or
        ``'appoggiatura'``.

        Returns ``'grace'``, ``'after'``, ``'acciaccatura'`` or
        ``'appoggiatura'``.
        '''
        return self._kind

    @kind.setter
    def kind(self, arg):
        assert arg in (
            'after',
            'grace',
            'acciaccatura',
            'appoggiatura',
            )
        self._kind = arg