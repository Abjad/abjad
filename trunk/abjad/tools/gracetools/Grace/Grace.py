from abjad.tools.containertools.Container import Container
from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools.gracetools.Grace._GraceFormatter import _GraceFormatter


class Grace(Container):
    r'''Abjad model of grace music::

        abjad> voice = Voice("c'8 d'8 e'8 f'8")
        abjad> spannertools.BeamSpanner(voice[:])
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        abjad> f(voice)
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        abjad> grace_notes = [Note("c'16"), Note("d'16")]
        abjad> gracetools.Grace(grace_notes, kind = 'grace')(voice[1])
        Note("d'8")

    ::

        abjad> f(voice)
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

        abjad> after_grace_notes = [Note("e'16"), Note("f'16")]
        abjad> gracetools.Grace(after_grace_notes, kind = 'after')(voice[1])
        Note("d'8")

    ::

        abjad> f(voice)
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

    Use ``Grace()`` to attach grace containers to nongrace notes, rests and chords.
    '''

    def __init__(self, music = None, kind = 'grace', **kwargs):
        # self._carrier is a reference to the Note carrying the Graces.
        self._carrier = None
        Container.__init__(self, music)
        self._formatter = _GraceFormatter(self)
        #self.kind = 'grace'
        self.kind = kind
        self._initialize_keyword_values(**kwargs)

    ### OVERLOADS ###

    def __call__(self, arg):
        if not isinstance(arg, _Leaf):
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

    ### PUBLIC ATTRIBUTES ###

    @apply
    def kind():
        def fget(self):
            r'''Get `kind` of grace container::

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> gracetools.Grace([Note("cs'16")], kind = 'grace')(staff[1])
                Note("d'8")
                abjad> grace_container = staff[1].grace
                abjad> grace_container.kind
                'grace'

            Return string.

            Set `kind` of grace container::

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> gracetools.Grace([Note("cs'16")], kind = 'grace')(staff[1])
                Note("d'8")
                abjad> grace_container = staff[1].grace
                abjad> grace_container.kind = 'acciaccatura'
                abjad> grace_container.kind
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

            abjad> staff = Staff("c'8 d'8 e'8 f'8")
            abjad> grace_container = gracetools.Grace([Note("cs'16")], kind = 'grace')
            abjad> grace_container(staff[1])
            Note("d'8")
            abjad> f(staff)
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

            abjad> grace_container.detach()
            Grace()
            abjad> f(staff)
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
