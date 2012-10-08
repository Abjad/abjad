from abjad.tools.resttools.Rest import Rest


class MultiMeasureRest(Rest):
    '''.. versionadded:: 2.0

    Abjad model of a multi-measure rest::

        >>> resttools.MultiMeasureRest((1, 4))
        MultiMeasureRest('R4')

    Multi-measure rests are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    _default_mandatory_input_arguments = ((1, 4), )

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        return 'R%s' % self._formatted_duration

    ### PUBLIC PROPERTIES ###

    @property
    def _body(self):
        '''Read-only list of string representation of body of rest.
        Picked up as format contribution at format-time.
        '''
        result = 'R' + str(self._formatted_duration)
        return [result]
