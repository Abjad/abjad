# -*- encoding: utf-8 -*-
from abjad.tools.scoretools.Leaf import Leaf


class MultimeasureRest(Leaf):
    '''A multimeasure rest.

    ::

        >>> rest = scoretools.MultimeasureRest((1, 4))
        >>> show(rest) # doctest: +SKIP

    Multimeasure rests are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _default_positional_input_arguments = (
        (1, 4),
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import scoretools
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
