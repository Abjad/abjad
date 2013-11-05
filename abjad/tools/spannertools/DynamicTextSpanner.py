# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.Spanner import Spanner


class DynamicTextSpanner(Spanner):
    r'''A dynamic text spanner.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> spanner = spannertools.DynamicTextSpanner(mark='f')
        >>> attach(spanner, staff[:])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 \f
            d'8
            e'8
            f'8
        }

    Format dynamic `mark` at first leaf in spanner.

    Returns dynamic text spanner.
    '''

    ### INTIALIZER ###

    def __init__(
        self, 
        components=None, 
        mark='',
        overrides=None,
        ):
        Spanner.__init__(
            self, 
            components,
            overrides=overrides,
            )
        self.mark = mark

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new.mark = self.mark

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(r'\%s' % self.mark)
        return result

    ### PUBLIC PROPERTIES ###

    @apply
    def mark():
        def fget(self):
            r'''Get dynamic string:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.DynamicTextSpanner(mark='f')
                >>> attach(spanner, staff[:])
                >>> spanner.mark
                'f'

            Set dynamic string:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.DynamicTextSpanner(mark='f')
                >>> attach(spanner, staff[:])
                >>> spanner.mark = 'p'
                >>> spanner.mark
                'p'

            Set string.
            '''
            return self._mark
        def fset(self, arg):
            assert isinstance(arg, str)
            self._mark = arg
        return property(**locals())
