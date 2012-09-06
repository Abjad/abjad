from abjad.tools.schemetools.Scheme import Scheme


class SchemeColor(Scheme):
    '''Abjad model of Scheme color::

        >>> schemetools.SchemeColor('ForestGreen')
        SchemeColor('ForestGreen')

    Scheme colors are immutable.
    '''

    ### CLASS ATTRIBUTES ##

    __slots__ = ()

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_value(self):
        return "(x11-color '%s)" % self._value
