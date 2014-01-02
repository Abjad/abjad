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

    ### CLASS VARIABLES ###

    __slots__ = (
        '_dynamic',
        )

    ### INTIALIZER ###

    def __init__(
        self, 
        dynamic='',
        overrides=None,
        ):
        Spanner.__init__(
            self, 
            overrides=overrides,
            )
        assert isinstance(dynamic, str)
        self._dynamic = dynamic

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new.dynamic = self.dynamic

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            string = r'\{}'.format(self.dynamic)
            result.append(string)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def dynamic(self):
        r'''Gets dynamic string.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.DynamicTextSpanner(dynamic='f')
                >>> attach(spanner, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> spanner.dynamic
                'f'

        Returns string.
        '''
        return self._dynamic
