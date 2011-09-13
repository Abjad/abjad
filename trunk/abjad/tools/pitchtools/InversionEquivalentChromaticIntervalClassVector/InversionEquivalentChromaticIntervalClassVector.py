from abjad.tools.pitchtools._Vector import _Vector


class InversionEquivalentChromaticIntervalClassVector(_Vector):
    '''.. versionadded:: 2.0

    Abjad model of inversion-equivalent chromatic interval-class vector::

        abjad> pitchtools.InversionEquivalentChromaticIntervalClassVector([1, 1, 6, 2, 2, 2])
        InversionEquivalentChromaticIntervalClassVector(0 | 2 3 0 0 0 1)

    Initialize by inversion-equivalent chromatic interval-class counts::

        abjad> pitchtools.InversionEquivalentChromaticIntervalClassVector(counts = [2, 3, 0, 0, 0, 1])
        InversionEquivalentChromaticIntervalClassVector(0 | 2 3 0 0 0 1)

    Inversion-equivalent chromatic interval-class vectors are immutable.
    '''

    def __init__(self, *args, **kwargs):
        from abjad.tools import pitchtools
        for icn in range(7):
            dict.__setitem__(self, icn, 0)
            dict.__setitem__(self, icn + 0.5, 0)
        dict.__delitem__(self, 6.5)
        if len(args) == 1:
            interval_class_tokens = args[0]
            for token in interval_class_tokens:
                interval_class_number = \
                    pitchtools.InversionEquivalentChromaticIntervalClass(token).number
                current_tally = self[interval_class_number]
                dict.__setitem__(self, interval_class_number, current_tally + 1)
        elif 'counts' in kwargs.keys():
            counts = kwargs['counts']
            assert len(counts) in (6, 7)
            if len(counts) == 6:
                keys = range(1, 7)
            elif len(counts) == 7:
                keys = range(0, 7)
            for key, value in zip(keys, counts):
                dict.__setitem__(self, key, value)
        else:
            raise ValueError('can not initiailize vector.')

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        string = '%s | %s' % (
            self._unison_string, self._nonunison_twelve_tone_string)
        if self._has_quartertones:
            string += ' %s' % self._quartertone_string
        return string

    @property
    def _has_quartertones(self):
        return any([0 < item[1] for item in self._quartertone_items])

    @property
    def _nonunison_twelve_tone_string(self):
        return ' '.join(self._twelve_tone_string.split()[1:])

    @property
    def _quartertone_items(self):
        return [item for item in self.items() if isinstance(item[0], float)]

    @property
    def _quartertone_string(self):
        return ' '.join([
            str(item[1]) for item in sorted(self._quartertone_items)])

    @property
    def _twelve_tone_items(self):
        return [item for item in self.items() if isinstance(item[0], int)]

    @property
    def _twelve_tone_string(self):
        return ' '.join([
            str(item[1]) for item in sorted(self._twelve_tone_items)])

    @property
    def _unison_string(self):
        return self._twelve_tone_string.split()[0]
