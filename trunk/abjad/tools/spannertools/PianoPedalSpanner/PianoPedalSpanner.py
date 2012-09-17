from abjad.tools.spannertools.Spanner import Spanner


class PianoPedalSpanner(Spanner):
    r'''Abjad piano pedal spanner::

            >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

            >>> spannertools.PianoPedalSpanner(staff[:])
            PianoPedalSpanner(c'8, d'8, e'8, f'8)

    ::

            >>> f(staff)
            \new Staff {
                \set Staff.pedalSustainStyle = #'mixed
                c'8 \sustainOn
                d'8
                e'8
                f'8 \sustainOff
            }

    Return piano pedal spanner.
    '''

    ### CLASS ATTRIBUTES ###

    _kinds = {'sustain': (r'\sustainOn', r'\sustainOff'),
            'sostenuto':(r'\sostenutoOn', r'\sostenutoOff'),
            'corda': (r'\unaCorda', r'\treCorde')}

    _styles = ['text', 'bracket', 'mixed']

    ### INITIALIZER ###

    def __init__(self, components=None):
        Spanner.__init__(self, components)
        self.kind = 'sustain'
        self.style = 'mixed'

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new.kind = self.kind
        new.style = self.style

    def _format_before_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(r"\set Staff.pedalSustainStyle = #'%s" % self.style)
        return result

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(self._kinds[self.kind][0])
        if self._is_my_last_leaf(leaf):
            result.append(self._kinds[self.kind][1])
        return result

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def kind():
        def fget(self):
            r'''Get piano pedal spanner kind::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.PianoPedalSpanner(staff[:])
                >>> spanner.kind
                'sustain'

            Set piano pedal spanner kind::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.PianoPedalSpanner(staff[:])
                >>> spanner.kind = 'sostenuto'
                >>> spanner.kind
                'sostenuto'

            Acceptable values ``'sustain'``, ``'sostenuto'``, ``'corda'``.
            '''
            return self._kind
        def fset(self, arg):
            if not arg in self._kinds.keys():
                raise ValueError("Type must be in %s" % self._kinds.keys())
            self._kind = arg
        return property(**locals())

    @apply
    def style():
        def fget(self):
            r'''Get piano pedal spanner style::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.PianoPedalSpanner(staff[:])
                >>> spanner.style
                'mixed'

            Set piano pedal spanner style::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.PianoPedalSpanner(staff[:])
                >>> spanner.style = 'bracket'
                >>> spanner.style
                'bracket'

            Acceptable values ``'mixed'``, ``'bracket'``, ``'text'``.
            '''
            return self._style
        def fset(self, arg):
            if not arg in self._styles:
                raise ValueError("Style must be in %s" % self._styles)
            self._style = arg
        return property(**locals())
