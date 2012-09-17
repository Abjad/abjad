from abjad.tools import pitchtools
from abjad.tools.spannertools.Spanner import Spanner


class TrillSpanner(Spanner):
    r'''Abjad trill spanner::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> spannertools.TrillSpanner(staff[:])
        TrillSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 \startTrillSpan
            d'8
            e'8
            f'8 \stopTrillSpan
        }

    Override LilyPond TrillSpanner grob.

    Return trill spanner.
    '''

    ### INITIALIZER ###

    def __init__(self, components=None):
        Spanner.__init__(self, components)
        self._pitch = None

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new.written_pitch = self.written_pitch

    def _format_before_leaf(self, leaf):
        result = []
        if self.pitch is not None:
            if self._is_my_first_leaf(leaf):
                result.append(r'\pitchedTrill')
        return result

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(r'\startTrillSpan')
            if self.pitch is not None:
                result.append(str(self.pitch))
        if self._is_my_last_leaf(leaf):
            result.append(r'\stopTrillSpan')
        return result

    ### PUBLIC PROPERTIES ###

    @apply
    def pitch():
        def fget(self):
            r'''Optional read / write pitch for pitched trills.

                ::

                    >>> t = Staff("c'8 d'8 e'8 f'8")
                    >>> trill = spannertools.TrillSpanner(t[:2])
                    >>> trill.pitch = pitchtools.NamedChromaticPitch('cs', 4)

                ::

                    >>> f(t)
                    \new Staff {
                        \pitchedTrill c'8 \startTrillSpan cs'
                        d'8 \stopTrillSpan
                        e'8
                        f'8
                    }

            Set pitch.
            '''
            return self._pitch
        def fset(self, expr):
            if expr is None:
                self._pitch = expr
            else:
                pitch = pitchtools.NamedChromaticPitch(expr)
                self._pitch = pitch
        return property(**locals())

    @apply
    def written_pitch():
        def fget(self):
            return self.pitch
        def fset(self, arg):
            self.pitch = arg
        return property(**locals())
