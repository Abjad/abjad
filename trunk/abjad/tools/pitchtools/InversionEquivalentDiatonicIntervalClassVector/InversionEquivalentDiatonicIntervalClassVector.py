from abjad.tools.pitchtools.ObjectVector import ObjectVector
from abjad.tools.pitchtools.inventory_inversion_equivalent_diatonic_interval_classes import \
    inventory_inversion_equivalent_diatonic_interval_classes
from abjad.tools.pitchtools.list_harmonic_diatonic_intervals_in_expr import \
    list_harmonic_diatonic_intervals_in_expr


class InversionEquivalentDiatonicIntervalClassVector(ObjectVector):
    '''.. versionadded:: 2.0

    Abjad model of inversion-equivalent diatonic interval-class vector::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8")
        >>> vector = pitchtools.InversionEquivalentDiatonicIntervalClassVector(staff)

    ::

        >>> print vector
        {P1: 0, aug1: 0, m2: 1, M2: 3, aug2: 0, dim3: 0, m3: 2, M3: 1, dim4: 0, P4: 3, aug4: 0}

    Inversion-equivalent diatonic interval-class vector are not quatertone-aware.

    Inversion-equivalent diatonic interval-class vectors are immutable.
    '''

    def __init__(self, expr):
        object.__setattr__(self, 'all_dics', inventory_inversion_equivalent_diatonic_interval_classes())
        for dic in self.all_dics:
            dict.__setitem__(self, dic, 0)
        for hdi in list_harmonic_diatonic_intervals_in_expr(expr):
            dic = hdi.diatonic_interval_class
            dict.__setitem__(self, dic, self[dic] + 1)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self._contents_string == arg._contents_string:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._contents_string)

    def __str__(self):
        return '{%s}' % self._contents_string

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_string(self):
        parts = []
        for dic in self.all_dics:
            count = self[dic]
            part = '%s: %s' % (dic, count)
            parts.append(part)
        contents_string = ', '.join(parts)
        return contents_string
