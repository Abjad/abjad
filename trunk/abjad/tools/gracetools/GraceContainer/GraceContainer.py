from abjad.tools.containertools.Container import Container
from abjad.tools.leaftools.Leaf import Leaf


class GraceContainer(Container):
    r'''Abjad model of grace music::

        >>> voice = Voice("c'8 d'8 e'8 f'8")
        >>> beamtools.BeamSpanner(voice[:])
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(voice)
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> grace_notes = [Note("c'16"), Note("d'16")]
        >>> gracetools.GraceContainer(grace_notes, kind='grace')(voice[1])
        Note("d'8")

    ::

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
        >>> gracetools.GraceContainer(after_grace_notes, kind='after')(voice[1])
        Note("d'8")

    ::

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


    Grace objects are containers you can fill with notes, rests and chords.

    Grace containers override the special ``__call__`` method.

    Use ``GraceContainer()`` to attach grace containers to nongrace notes, rests and chords.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_carrier', '_kind', )

    ### INITIALIZER ###

    def __init__(self, music=None, kind='grace', **kwargs):
        # self._carrier is a reference to the leaf carrying grace music
        self._carrier = None
        Container.__init__(self, music)
        self.kind = kind
        self._initialize_keyword_values(**kwargs)

    ### SPECIAL METHODS ###

    def __call__(self, arg):
        if not isinstance(arg, Leaf):
            raise TypeError('object to which grace container attaches much be leaf: "%s".' % arg)
        if self.kind == 'after':
            arg._after_grace = self
            arg.after_grace = self
        else:
            arg._grace = self
            arg.grace = self
        self._carrier = arg
        return arg

    def __copy__(self, *args):
        new = Container.__copy__(self, *args)
        new.kind = self.kind
        return new

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._summary)

    ### PRIVATE METHODS ###

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

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        self._update_marks_of_entire_score_tree_if_necessary()
        return self._format_component()

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def kind():
        def fget(self):
            r'''Get `kind` of grace container::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> gracetools.GraceContainer([Note("cs'16")], kind = 'grace')(staff[1])
                Note("d'8")
                >>> grace_container = staff[1].grace
                >>> grace_container.kind
                'grace'

            Return string.

            Set `kind` of grace container::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> gracetools.GraceContainer([Note("cs'16")], kind = 'grace')(staff[1])
                Note("d'8")
                >>> grace_container = staff[1].grace
                >>> grace_container.kind = 'acciaccatura'
                >>> grace_container.kind
                'acciaccatura'

            Set string.

            Valid options include ``'after'``, ``'grace'``, ``'acciaccatura'``, ``'appoggiatura'``.
            '''
            return self._kind
        def fset(self, arg):
            assert arg in ('after', 'grace', 'acciaccatura', 'appoggiatura')
            self._kind = arg
        return property(**locals())

    ### PUBLIC METHODS ###

    def detach(self):
        r'''Detach grace container from leaf::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> grace_container = gracetools.GraceContainer([Note("cs'16")], kind = 'grace')
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

        Return grace container.
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
