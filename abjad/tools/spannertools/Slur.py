# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.spannertools.Spanner import Spanner


class Slur(Spanner):
    r'''A slur spanner.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> slur = spannertools.Slur()
        >>> attach(slur, staff[:])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }

    '''

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        direction=None,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            components,
            overrides=overrides,
            )
        self.direction = direction

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new.direction = self.direction

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            direction = self.direction
            if direction is not None:
                result.append('{} ('.format(
                    stringtools.arg_to_tridirectional_lilypond_symbol(
                        direction)))
            else:
                result.append('(')
        if self._is_my_last_leaf(leaf):
            result.append(')')
        return result

    ### PUBLIC PROPERTIES ###

    @apply
    def direction():
        def fget(self):
            return self._direction
        def fset(self, arg):
            self._direction = \
                stringtools.arg_to_tridirectional_lilypond_symbol(arg)
        return property(**locals())
