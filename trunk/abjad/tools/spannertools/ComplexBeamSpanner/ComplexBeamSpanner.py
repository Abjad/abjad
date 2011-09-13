from abjad.tools.spannertools.BeamSpanner.BeamSpanner import BeamSpanner
from abjad.tools.spannertools.ComplexBeamSpanner._ComplexBeamSpannerFormatInterface import _ComplexBeamSpannerFormatInterface


class ComplexBeamSpanner(BeamSpanner):
    r'''Abjad complex beam spanner::

        abjad> staff = Staff("c'16 e'16 r16 f'16 g'2")

    ::

        abjad> f(staff)
        \new Staff {
            c'16
            e'16
            r16
            f'16
            g'2
        }

    ::

        abjad> spannertools.ComplexBeamSpanner(staff[:4])
        ComplexBeamSpanner(c'16, e'16, r16, f'16)

    ::

        abjad> f(staff)
        \new Staff {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #2
            e'16 ]
            r16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            f'16 [ ]
            g'2
        }

    Return complex beam spanner.
    '''

    def __init__(self, components = None, lone = False):
        BeamSpanner.__init__(self, components = components)
        self._format = _ComplexBeamSpannerFormatInterface(self)
        self.lone = lone

    ### PUBLIC ATTRIBUTES ###

    @apply
    def lone():
        def fget(self):
            r'''Beam lone leaf and force beam nibs to left::

                abjad> note = Note("c'16")

            ::

                abjad> beam = spannertools.ComplexBeamSpanner([note], lone = 'left')

            ::

                abjad> f(note)
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #0
                c'16 [ ]

            Beam lone leaf and force beam nibs to right::

                abjad> note = Note("c'16")

            ::

                abjad> beam = spannertools.ComplexBeamSpanner([note], lone = 'right')

            ::

                abjad> f(note)
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #2
                c'16 [ ]

            Beam lone leaf and force beam nibs to both left and right::

                abjad> note = Note("c'16")

            ::

                abjad> beam = spannertools.ComplexBeamSpanner([note], lone = 'both')

            ::

                abjad> f(note)
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #2
                c'16 [ ]

            Beam lone leaf and accept LilyPond default nibs at both left and right::

                abjad> note = Note("c'16")

            ::

                abjad> beam = spannertools.ComplexBeamSpanner([note], lone = True)

            ::

                abjad> f(note)
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #2
                c'16 [ ]

            Do not beam lone leaf::

                abjad> note = Note("c'16")

            ::

                abjad> beam = spannertools.ComplexBeamSpanner([note], lone = False)

            ::

                abjad> f(note)
                c'16

            Set to ``'left'``, ``'right'``, ``'both'``, true or false as shown above.

            Ignore this setting when spanner contains more than one leaf.
            '''
            return self._lone
        def fset(self, arg):
            assert isinstance(arg, bool) or arg in ('left', 'right', 'both')
            self._lone = arg
        return property(**locals())
