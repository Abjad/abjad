# -*- encoding: utf-8 -*-
from abjad.tools.resttools.Rest import Rest


class MultimeasureRest(Rest):
    '''Abjad model of a multi-measure rest:

    ::

        >>> resttools.MultimeasureRest((1, 4))
        MultimeasureRest('R4')

    Multi-measure rests are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _default_positional_input_arguments = (
        (1, 4),
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
