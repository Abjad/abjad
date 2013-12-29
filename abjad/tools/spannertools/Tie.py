# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.spannertools.Spanner import Spanner


class Tie(Spanner):
    r'''A tie.

    ::

        >>> staff = Staff(scoretools.make_repeated_notes(4))
        >>> tie = spannertools.Tie()
        >>> attach(tie, staff[:])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
        }

    '''

    ### INITIALIZER ###

    def __init__(
        self,
        direction=None,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        self.direction = direction

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new.direction = self.direction

    def _format_right_of_leaf(self, leaf):
        result = []
        if not self._is_my_last_leaf(leaf):
            if self.direction is not None:
                result.append('{} ~'.format(
                    stringtools.arg_to_tridirectional_lilypond_symbol(
                    self.direction)))
            else:
                result.append('~')
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets and sets direction of tie.

        Returns up, down or none.
        '''
        return self._direction

    @direction.setter
    def direction(self, arg):
        self._direction = \
            stringtools.arg_to_tridirectional_lilypond_symbol(arg)
