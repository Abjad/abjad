from abjad.tools.spannertools.Spanner import Spanner


class OctavationSpanner(Spanner):
    r'''Abjad octavation spanner::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> spanner = spannertools.OctavationSpanner(staff[:], start=1)

    ::

        >>> f(staff)
        \new Staff {
            \ottava #1
            c'8
            d'8
            e'8
            f'8
            \ottava #0
        }

    Return octavation spanner.
    '''

    ### INITIALIZER ###

    # TODO: Set start to 1 (and stop to 0) by default. #
    def __init__(self, components=None, start=0, stop=0):
        Spanner.__init__(self, components)
        self.start = start
        self.stop = stop

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new.start = self.start
        new.stop = self.stop

    def _format_after_leaf(self, leaf):
        result = []
        result.extend(Spanner._format_after_leaf(self, leaf))
        if self._is_my_last_leaf(leaf):
            result.append(r'\ottava #%s' % self.stop)
        return result

    def _format_before_leaf(self, leaf):
        result = []
        result.extend(Spanner._format_before_leaf(self, leaf))
        if self._is_my_first_leaf(leaf):
            result.append(r'\ottava #%s' % self.start)
        return result

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def start():
        def fget(self):
            r'''Get octavation start::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> octavation = spannertools.OctavationSpanner(staff[:], start=1)
                >>> octavation.start
                1

            Set octavation start::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> octavation = spannertools.OctavationSpanner(staff[:], start=1)
                >>> octavation.start
                1

            Set integer.
            '''
            return self._start
        def fset(self, arg):
            assert isinstance(arg, (int, type(None)))
            self._start = arg
        return property(**locals())

    @apply
    def stop():
        def fget(self):
            r'''Get octavation stop::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> octavation = spannertools.OctavationSpanner(staff[:], start=2, stop=1)
                >>> octavation.stop
                1

            Set octavation stop::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> octavation = spannertools.OctavationSpanner(staff[:], start=2, stop=1)
                >>> octavation.stop = 0
                >>> octavation.stop
                0

            Set integer.
            '''
            return self._stop
        def fset(self, arg):
            assert isinstance(arg, (int, type(None)))
            self._stop = arg
        return property(**locals())
