from abjad.tools.spannertools.Spanner import Spanner


class DynamicTextSpanner(Spanner):
    r'''Abjad dynamic text spanner::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> spannertools.DynamicTextSpanner(staff[:], 'f')
        DynamicTextSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 \f
            d'8
            e'8
            f'8
        }

    Format dynamic `mark` at first leaf in spanner.

    Return dynamic text spanner.
    '''

    ### INTIALIZER ###

    def __init__(self, components=None, mark=''):
        Spanner.__init__(self, components)
        self.mark = mark

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new.mark = self.mark

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(r'\%s' % self.mark)
        return result

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def mark():
        def fget(self):
            '''Get dynamic string::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> dynamic_text_spanner = spannertools.DynamicTextSpanner(staff[:], 'f')
                >>> dynamic_text_spanner.mark
                'f'

            Set dynamic string::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> dynamic_text_spanner = spannertools.DynamicTextSpanner(staff[:], 'f')
                >>> dynamic_text_spanner.mark = 'p'
                >>> dynamic_text_spanner.mark
                'p'

            Set string.
            '''
            return self._mark
        def fset(self, arg):
            assert isinstance(arg, str)
            self._mark = arg
        return property(**locals())
