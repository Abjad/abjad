from abjad.tools.schemetools.Scheme import Scheme


class SchemeColor(Scheme):
    '''Abjad model of Scheme color::

        abjad> schemetools.SchemeColor('ForestGreen')
        SchemeColor('ForestGreen')

    Scheme colors are immutable.
    '''

    ### PRIVATE ATTRIBUTES ###

    @property
    def _formatted_value(self):
        return "(x11-color '%s)" % self._value
