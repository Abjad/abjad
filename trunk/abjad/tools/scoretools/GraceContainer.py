# -*- encoding: utf-8 -*-
from abjad.tools.scoretools.Container import Container


class GraceContainer(Container):
    r'''A container of grace music.

    ::

        >>> voice = Voice("c'8 d'8 e'8 f'8")
        >>> beam = spannertools.BeamSpanner()
        >>> attach(beam, voice[:])
        >>> show(voice) # doctest: +SKIP

    ..  doctest::

        >>> f(voice)
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> grace_notes = [Note("c'16"), Note("d'16")]
        >>> scoretools.GraceContainer(grace_notes, kind='grace')(voice[1])
        Note("d'8")
        >>> show(voice) # doctest: +SKIP

    ..  doctest::

        >>> f(voice)
        \new Voice {
            c'8 [
            \grace {
                c'16
                d'16
            }
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> after_grace_notes = [Note("e'16"), Note("f'16")]
        >>> scoretools.GraceContainer(
        ...     after_grace_notes, kind='after')(voice[1])
        Note("d'8")
        >>> show(voice) # doctest: +SKIP

    ..  doctest::

        >>> f(voice)
        \new Voice {
            c'8 [
            \grace {
                c'16
                d'16
            }
            \afterGrace
            d'8
            {
                e'16
                f'16
            }
            e'8
            f'8 ]
        }

    Fill grace containers with notes, rests or chords.

    Attach grace containers to nongrace notes, rests or chords.
    '''

    ### CLASS VARIABLES ###

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

    ### SPECIAL METHODS ###

    def __call__(self, arg):
        from abjad.tools import scoretools
        if not isinstance(arg, scoretools.Leaf):
            message = 'object to which grace container attaches'
            message += ' must be leaf: "%s".'
            message = message.format(arg)
            raise TypeError(message)
        if self.kind == 'after':
            arg._after_grace = self
            arg.after_grace = self
        else:
            arg._grace = self
            arg.grace = self
        self._carrier = arg
        return arg

    def __repr__(self):
        return '{}({})'.format(self._class_name, self._summary)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        self._update_now(marks=True)
        return self._format_component()

    ### PRIVATE METHODS ###

    def _copy_with_marks_but_without_children_or_spanners(self):
        new = Container._copy_with_marks_but_without_children_or_spanners(self)
        new.kind = self.kind
        return new

    def _format_open_brackets_slot(self, format_contributions):
        result = []
        kind = self.kind
        if kind == 'after':
            result.append([('grace_brackets', 'open'), ['{']])
        else:
            contributor = ('grace_brackets', 'open')
            contributions = [r'\%s {' % kind]
            result.append([contributor, contributions])
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @apply
    def kind():
        def fget(self):
            r'''Gets `kind` of grace container.

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> scoretools.GraceContainer(
                ...     [Note("cs'16")], kind = 'grace')(staff[1])
                Note("d'8")
                >>> grace_container = staff[1].grace
                >>> grace_container.kind
                'grace'

            Returns string.

            Sets `kind` of grace container:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> scoretools.GraceContainer(
                ...     [Note("cs'16")], kind = 'grace')(staff[1])
                Note("d'8")
                >>> grace_container = staff[1].grace
                >>> grace_container.kind = 'acciaccatura'
                >>> grace_container.kind
                'acciaccatura'

            Sets string.

            Valid options include ``'after'``, ``'grace'``, 
            ``'acciaccatura'``, ``'appoggiatura'``.
            '''
            return self._kind
        def fset(self, arg):
            assert arg in (
                'after',
                'grace',
                'acciaccatura',
                'appoggiatura',
                )
            self._kind = arg
        return property(**locals())

    ### PUBLIC METHODS ###

    def _attach(self, leaf):
        r'''Attaches grace container to `leaf`.

        Returns grace container.
        '''
        return self(leaf)

    def detach(self):
        r'''Detaches grace container from leaf.

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> grace_container = scoretools.GraceContainer(
            ...     [Note("cs'16")], kind = 'grace')
            >>> grace_container(staff[1])
            Note("d'8")
            >>> f(staff)
            \new Staff {
                c'8
                \grace {
                    cs'16
                }
                d'8
                e'8
                f'8
            }

        ::

            >>> grace_container.detach()
            GraceContainer()
            >>> f(staff)
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }

        Returns grace container.
        '''
        if self._carrier is not None:
            carrier = self._carrier
            if self.kind == 'after':
                delattr(carrier, '_after_grace')
                delattr(carrier, 'after_grace')
            else:
                delattr(carrier, '_grace')
                delattr(carrier, 'grace')
            self._carrier = None
            self[:] = []
        return self
