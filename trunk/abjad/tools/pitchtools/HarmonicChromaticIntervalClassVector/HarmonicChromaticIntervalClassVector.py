from abjad.tools.pitchtools._Vector import _Vector
from abjad.tools.pitchtools.list_harmonic_chromatic_intervals_in_expr import list_harmonic_chromatic_intervals_in_expr


class HarmonicChromaticIntervalClassVector(_Vector):
    '''.. versionadded:: 2.0

    Abjad model of harmonic chromatic interval-class vector::

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8")
        abjad> hcicv = pitchtools.HarmonicChromaticIntervalClassVector(staff)
        abjad> print hcicv
        0 1 3 2 1 2 0 1 0 0 0 0

    Harmonic chromatic interval-class vector is quartertone-aware::

        abjad> staff.append(Note(1.5, (1, 4)))
        abjad> hcicv = pitchtools.HarmonicChromaticIntervalClassVector(staff)
        abjad> print hcicv
        0 1 3 2 1 2 0 1 0 0 0 0
        1 1 1 1 0 1 0 0 0 0 0 0

    Harmonic chromatic interval-class vectors are immutable.
    '''

    def __init__(self, expr):
        for interval_number in range(12):
            dict.__setitem__(self, interval_number, 0)
            dict.__setitem__(self, interval_number + 0.5, 0)
        for chromatic_interval in list_harmonic_chromatic_intervals_in_expr(expr):
            interval_number = chromatic_interval.harmonic_chromatic_interval_class.number
            current_tally = self[interval_number]
            dict.__setitem__(self, interval_number, current_tally + 1)

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._contents_string)

    def __setitem__(self, *args):
        raise AttributeError('%s objects are immutable.' % type(self).__name__)

    def __str__(self):
        items = self.items()
        twelve_tone_counts = [
            item for item in items if isinstance(item[0], int)]
        twelve_tone_counts.sort()
        twelve_tone_string = ' '.join([str(x[1]) for x in twelve_tone_counts])
        if self._has_quartertones:
            items = [item for item in items if isinstance(item[0], float)]
            items.sort()
            quartertone_string = ' '.join([str(item[1]) for item in items])
            return '%s\n%s' % (twelve_tone_string, quartertone_string)
        return twelve_tone_string

    ### PRIVATE ATTRIBUTES ###

    @property
    def _contents_string(self):
        items = self.items()
        if not self._has_quartertones:
            items = [item for item in items if isinstance(item[0], int)]
        items.sort()
        contents_string = ['%s: %s' % item for item in items]
        contents_string = ', '.join(contents_string)
        return contents_string

    @property
    def _has_quartertones(self):
        for interval_number in range(12):
            if self[interval_number + 0.5]:
                return True
        return False

    ### PUBLIC METHODS ###

    def has_none_of(self, chromatic_interval_numbers):
        '''True when harmonic chromatic interval-class vector contains none of
        `chromatic_interval_numbers`. Otherwise false::

            abjad> hcicv = pitchtools.HarmonicChromaticIntervalClassVector(Staff("c'8 d'8 e'8 f'8 g'8"))
            abjad> hcicv.has_none_of([9, 10, 11])
            True

        Return boolean.
        '''
        for chromatic_interval_number in chromatic_interval_numbers:
            if self[chromatic_interval_number]:
                return False
        return True
