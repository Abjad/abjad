# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.Spanner import Spanner


class DynamicTextSpanner(Spanner):
    r'''A dynamic text spanner.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> spanner = spannertools.DynamicTextSpanner(dynamic='f')
        >>> attach(spanner, staff[:])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            c'8 \f
            d'8
            e'8
            f'8
        }

    Formats `dynamic` on first leaf in spanner.
    '''

    ### INTIALIZER ###

    def __init__(
        self, 
        components=None, 
        dynamic='',
        overrides=None,
        ):
        Spanner.__init__(
            self, 
            components,
            overrides=overrides,
            )
        self.dynamic = dynamic

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new.dynamic = self.dynamic

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(r'\{}'.format(self.dynamic))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def dynamic(self):
        r'''Get dynamic string:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.DynamicTextSpanner(dynamic='f')
            >>> attach(spanner, staff[:])
            >>> spanner.dynamic
            'f'

        Set dynamic string:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.DynamicTextSpanner(dynamic='f')
            >>> attach(spanner, staff[:])
            >>> spanner.dynamic = 'p'
            >>> spanner.dynamic
            'p'

        Set string.
        '''
        return self._dynamic

    @dynamic.setter
    def dynamic(self, arg):
        assert isinstance(arg, str)
        self._dynamic = arg
