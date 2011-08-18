from abjad.tools.resttools.Rest import Rest
from abjad.tools.leaftools._Leaf import _Leaf


class MultiMeasureRest(Rest):
    '''.. versionadded:: 2.0

    Abjad model of a multi-measure rest::

        abjad> resttools.MultiMeasureRest((1, 4))
        MultiMeasureRest('R4')

    Multi-measure rests are immutable.
    '''

    __slots__ = ()

    ### PRIVATE ATTRIBUTES ###

    @property
    def _compact_representation(self):
        return 'R%s' % self._formatted_duration

    ### PUBLIC ATTRIBUTES ###

    @property
    def _body(self):
        '''Read-only list of string representation of body of rest.
        Picked up as format contribution at format-time.'''
        result = 'R' + str(self._formatted_duration)
        return [result]
