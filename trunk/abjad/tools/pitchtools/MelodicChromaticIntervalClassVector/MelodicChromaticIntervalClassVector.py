from abjad.tools.pitchtools._Vector import _Vector


class MelodicChromaticIntervalClassVector(_Vector):
    '''.. versionadded:: 2.0

    Abjad model of melodic chromatic interval-class vector::

        abjad> print pitchtools.MelodicChromaticIntervalClassVector([-2, -14, 3, 5.5, 6.5])
            .   |   .   .   1   .   .   .   |   .   .   .   .   .   .
                |   .   2   .   .   .   .   |   .   .   .   .   .   .
                |   .   .   .   .   .   1   |   1   .   .   .   .   .
                |   .   .   .   .   .   .   |   .   .   .   .   .   .

    Melodic chromatic interval-class vectors are immutable.
    '''

    def __init__(self, mcic_tokens):
        from abjad.tools import pitchtools
        for mcicn in range(13):
            dict.__setitem__(self, mcicn, 0)
            dict.__setitem__(self, -mcicn, 0)
            dict.__setitem__(self, mcicn + 0.5, 0)
            dict.__setitem__(self, -(mcicn + 0.5), 0)
        dict.__delitem__(self, 12.5)
        dict.__delitem__(self, -12.5)
        for mcic_token in mcic_tokens:
            mcic = pitchtools.MelodicChromaticIntervalClass(mcic_token)
            dict.__setitem__(self, mcic.number, self[mcic.number] + 1)

    ### OVERLOADS ###

    def __len__(self):
        total_intervals = 0
        for mcic, count in self.items():
            total_intervals += count
        return total_intervals

    def __repr__(self):
        body = ', '.join(self._format_strings)
        return '%s(%s)' % (type(self).__name__, body)

    def __str__(self):
        return '\n'.join(self._format_strings)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_strings(self):
        strings = []
        strings.append(self._twelve_tone_ascending_string)
        strings.append(self._twelve_tone_descending_string)
        strings.append(self._quartertone_ascending_string)
        strings.append(self._quartertone_descending_string)
        return strings

    @property
    def _quartertone_ascending_string(self):
        counts = []
        for n in range(12):
            count = self[n + 0.5]
            if count == 0:
                counts.append('.')
            else:
                counts.append(count)
        left = counts[:6]
        right = counts[6:]
        left = ' '.join([str(x).rjust(3) for x in left])
        right = ' '.join([str(x).rjust(3) for x in right])
        zero = ' '.rjust(3)
        return '%s   | %s   | %s' % (zero, left, right)

    @property
    def _quartertone_descending_string(self):
        counts = []
        for n in range(12):
            count = self[-(n + 0.5)]
            if count == 0:
                counts.append('.')
            else:
                counts.append(count)
        left = counts[:6]
        right = counts[6:]
        left = ' '.join([str(x).rjust(3) for x in left])
        right = ' '.join([str(x).rjust(3) for x in right])
        zero = ' '.rjust(3)
        return '%s   | %s   | %s' % (zero, left, right)

    @property
    def _twelve_tone_ascending_string(self):
        counts = []
        for n in range(1, 13):
            count = self[n]
            if count == 0:
                counts.append('.')
            else:
                counts.append(count)
        left = counts[:6]
        right = counts[6:]
        left = ' '.join([str(x).rjust(3) for x in left])
        right = ' '.join([str(x).rjust(3) for x in right])
        if self[0] == 0:
            zero = '.'
        else:
            zero = str(self[0])
        zero = zero.rjust(3)
        return '%s   | %s   | %s' % (zero, left, right)

    @property
    def _twelve_tone_descending_string(self):
        counts = []
        for n in range(1, 13):
            count = self[-n]
            if count == 0:
                counts.append('.')
            else:
                counts.append(count)
        left = counts[:6]
        right = counts[6:]
        left = ' '.join([str(x).rjust(3) for x in left])
        right = ' '.join([str(x).rjust(3) for x in right])
        zero = ' '.rjust(3)
        return '%s   | %s   | %s' % (zero, left, right)
