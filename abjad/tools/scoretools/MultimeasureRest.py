# -*- coding: utf-8 -*-
from abjad.tools.scoretools.Leaf import Leaf


class MultimeasureRest(Leaf):
    '''A multimeasure rest.

    ::

        >>> rest = scoretools.MultimeasureRest((1, 4))
        >>> show(rest) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Leaves'

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import scoretools
        if len(args) == 0:
            args = ((1, 4),)
        rest = scoretools.Rest(*args)
        Leaf.__init__(
            self,
            rest.written_duration,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        return 'R%s' % self._formatted_duration

    ### PUBLIC PROPERTIES ###

    @property
    def _body(self):
        r'''List of string representation of body of rest.
        Picked up as format contribution at format-time.
        '''
        result = 'R' + str(self._formatted_duration)
        return [result]
